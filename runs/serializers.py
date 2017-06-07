
import uuid

from rest_framework import serializers

from .models import ContentChannel, ContentChannelRun, ChannelRunLog, ChannelRunEvent


class ContentChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentChannel
        # fields = '__all__'
        fields = ('channel_id', 'name', 'description', 'version', 'source_domain', 'source_id', 'user_registered_by', 'content_server')


class ContentChannelCreateSerializer(serializers.Serializer):
    channel_id = serializers.UUIDField()
    name = serializers.CharField(max_length=200, allow_blank=True)  # equiv to ricecooker's `title`
    description = serializers.CharField(max_length=400, allow_blank=True)
    version = serializers.IntegerField(default=0)
    source_domain = serializers.CharField(max_length=300, required=False, allow_blank=True)
    source_id = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)
    user_registered_by = serializers.EmailField(max_length=200, required=False, allow_blank=True, allow_null=True)
    user_token = serializers.CharField(max_length=200, required=False, allow_blank=True)
    content_server = serializers.URLField(max_length=300, default='https://develop.contentworkshop.learningequality.org')

    def create(self, validated_data):
        """
        Create and return a new `ContentChannel` instance, given the validated data.
        """
        return ContentChannel.objects.create(**validated_data)



class ContentChannelRunSerializer(serializers.ModelSerializer):
    channel = ContentChannelSerializer()
    class Meta:
        model = ContentChannelRun
        fields = ('run_id', 'channel', 'chef_name', 'ricecooker_version', 'state', 'started', 'finished', 'duration')

class ContentChannelRunCreateSerializer(serializers.Serializer):
    channel_id = serializers.CharField(write_only=True)      # need to supply channel_id when creating run  
    channel = ContentChannelSerializer(read_only=True)
    run_id = serializers.CharField(read_only=True)
    chef_name = serializers.CharField(max_length=200)
    ricecooker_version = serializers.CharField(max_length=100)
    # Denormalized info extracted from run events table
    state = serializers.CharField(read_only=True)
    started = serializers.DateTimeField(read_only=True)
    finished = serializers.DateTimeField(read_only=True)
    duration = serializers.DurationField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `ContentChannel` instance, given the validated data.
        """
        channel = ContentChannel.objects.get(channel_id=validated_data['channel_id'])
        del validated_data['channel_id']
        channel_run = ContentChannelRun.objects.create(channel=channel, **validated_data)
        runlog = ChannelRunLog(run=channel_run)
        runlog.save()
        return channel_run
