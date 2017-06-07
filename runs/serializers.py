
import uuid

from rest_framework import serializers

from .models import ContentChannel, ContentChannelRun, ChannelRunLog, ChannelRunEvent


class ContentChannelSerializer(serializers.ModelSerializer):
    channel_id = serializers.UUIDField(format='hex')
    class Meta:
        model = ContentChannel
        fields = ('channel_id', 'name', 'description', 'version', 'source_domain', 'source_id', 'user_registered_by', 'content_server')

class ContentChannelCreateSerializer(serializers.Serializer):
    channel_id = serializers.UUIDField(format='hex')
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
    run_id = serializers.UUIDField(format='hex', read_only=True)
    channel = ContentChannelSerializer(read_only=True)
    class Meta:
        model = ContentChannelRun
        fields = ('run_id', 'channel', 'chef_name', 'ricecooker_version', 'state', 'started', 'finished', 'duration')

class ContentChannelRunCreateSerializer(serializers.ModelSerializer):
    run_id = serializers.UUIDField(format='hex', read_only=True)
    channel_id = serializers.UUIDField(format='hex', write_only=True)   # need to supply channel_id when creating run
    channel = ContentChannelSerializer(read_only=True)
    # hostname ??? --> to store where sushi chef is running ???

    class Meta:
        model = ContentChannelRun
        read_only_fields = ('run_id', 'channel', 'state', 'started', 'finished', 'duration')
        fields = ('run_id', 'channel_id', 'channel', 'chef_name', 'ricecooker_version')

    def create(self, validated_data):
        """
        Create and return a new `ContentChannel` instance, given the validated data.
        """
        channel_id = validated_data.pop('channel_id')
        channel = ContentChannel.objects.get(channel_id=channel_id)
        channel_run = ContentChannelRun.objects.create(channel=channel, **validated_data)
        runlog = ChannelRunLog(run=channel_run)   # manually create runlog once we know the run_id
        runlog.save()
        return channel_run







class ChannelRunEventSerializer(serializers.ModelSerializer):
    run_id = serializers.UUIDField(source='run.run_id', format='hex', read_only=True)
    class Meta:
        model = ChannelRunEvent
        fields = ('id', 'run_id', 'event', 'progress', 'timestamp')

class ChannelRunEventCreateSerializer(serializers.ModelSerializer):
    run_id = serializers.UUIDField(format='hex')

    class Meta:
        model = ChannelRunEvent
        read_only_fields = ('id', )
        fields = ('id', 'run_id', 'event', 'progress', 'timestamp')

    def create(self, validated_data):
        """
        Create and return a new `ContentChannel` instance, given the validated data.
        """
        run_id = validated_data.pop('run_id')
        run = ContentChannelRun.objects.get(run_id=run_id)
        event = ChannelRunEvent.objects.create(run=run, **validated_data)
        return event


