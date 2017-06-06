
import uuid

from rest_framework import serializers

from .models import ContentChannel, ContentChannelRun, RunLogFile, ChannelRunEvent


class ContentChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentChannel
        # fields = '__all__'
        fields = ('id', 'channel_id', 'name', 'description', 'version', 'source_domain', 'source_id', 'user_registered_by', 'content_server')


class ContentChannelCreateSerializer(serializers.Serializer):
    channel_id = serializers.UUIDField(default=uuid.uuid4)
    name = serializers.CharField(max_length=200, allow_blank=True)  # equiv to ricecooker's `title`
    description = serializers.CharField(max_length=400, allow_blank=True)
    version = serializers.IntegerField(default=0)
    source_domain = serializers.CharField(max_length=300, required=False, allow_blank=True)
    source_id = serializers.CharField(max_length=200, required=False, allow_blank=True)
    user_registered_by = serializers.EmailField(max_length=200, required=False, allow_blank=True)
    user_token = serializers.CharField(max_length=200, required=False, allow_blank=True)
    content_server = serializers.URLField(max_length=300, default='https://develop.contentworkshop.learningequality.org')

    def create(self, validated_data):
        """
        Create and return a new `ContentChannel` instance, given the validated data.
        """
        return ContentChannel.objects.create(**validated_data)
