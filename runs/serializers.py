
import uuid

from rest_framework import serializers

from .models import ContentChannel, ContentChannelRun, ChannelRunStage



class ContentChannelSerializer(serializers.ModelSerializer):
    channel_id = serializers.UUIDField(format='hex')
    class Meta:
        model = ContentChannel
        fields = ('channel_id', 'name', 'description', 'version', 'source_domain', 'source_id',
                  'registered_by_user', 'registered_by_user_token', 'default_content_server')


class ContentChannelRunSerializer(serializers.ModelSerializer):
    run_id = serializers.UUIDField(format='hex', read_only=True)
    channel_id = serializers.UUIDField(format='hex', write_only=True)   # need to supply channel_id when creating run
    channel = ContentChannelSerializer(read_only=True)
    # hostname ??? --> to store where sushi chef is running ???

    class Meta:
        model = ContentChannelRun
        read_only_fields = ('run_id', 'channel')
        fields = ('run_id', 'channel_id', 'channel', 'chef_name', 'ricecooker_version',
                  'logfile', 'resource_counts', 'resource_sizes', 'extra_options',
                  'started_by_user', 'started_by_user_token', 'content_server', )

# Extra optional attributes like error counts, and command-line toggles (--staging / --publish / --update)


    def create(self, validated_data):
        """
        Create and return a new `ContentChannelRun` instance, given the validated data.
        """
        channel_id = validated_data.pop('channel_id')
        channel = ContentChannel.objects.get(channel_id=channel_id)
        channel_run = ContentChannelRun.objects.create(channel=channel, **validated_data)
        channel_run.save() # save again to greate runlog file with right filename
        return channel_run



class ChannelRunStageCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
