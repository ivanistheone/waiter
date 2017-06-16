

from rest_framework import serializers

from .models import ContentChannel, ContentChannelRun, ChannelRunStage



class ContentChannelSerializer(serializers.ModelSerializer):
    channel_id = serializers.UUIDField(format='hex')
    class Meta:
        model = ContentChannel
        fields = ('channel_id', 'name', 'description', 'version', 'source_domain', 'source_id',
                  'registered_by_user', 'registered_by_user_token', 'default_content_server')
        extra_kwargs = {
            'registered_by_user_token': {'write_only': True}
        }

class ContentChannelRunSerializer(serializers.ModelSerializer):
    run_id = serializers.UUIDField(format='hex', read_only=True)
    channel_id = serializers.UUIDField(format='hex', write_only=True)   # need to supply channel_id when creating run
    channel = ContentChannelSerializer(read_only=True)
    # hostname ??? --> to store where sushi chef is running ???

    class Meta:
        model = ContentChannelRun
        read_only_fields = ('run_id', 'channel', 'created_at')
        fields = ('run_id', 'channel_id', 'channel', 'chef_name', 'ricecooker_version', 'created_at',
                  'logfile', 'resource_counts', 'resource_sizes', 'extra_options',
                  'started_by_user', 'started_by_user_token', 'content_server', )
        extra_kwargs = {
            'started_by_user_token': {'write_only': True}
        }

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
    """
    MMVP stage receiver serializer for messages of the form:
    {
       'run_id': 'string',
       'stage': 'STAGENAME',                  # An identifier for the stage name
       'duration': duration,                  # in seconds  timedelta.total_seconds()
    }
    """
    run_id = serializers.CharField(max_length=100)
    stage = serializers.CharField(max_length=100)
    duration = serializers.FloatField()

class ChannelRunStageSerializer(serializers.ModelSerializer):
    """
    Serializer used to return response.
    """
    run_id = serializers.UUIDField(source='run.run_id', format='hex', read_only=True)
    duration = serializers.FloatField(source='get_duration_in_seconds')

    class Meta:
        model = ChannelRunStage
        read_only_fields = ('run_id',)
        fields = ('run_id', 'name', 'started', 'finished', 'duration')



class ChannelRunProgressSerializer(serializers.Serializer):
    """
    Run progress messages are of the form:
    {
       "run_id": "f2c0906a77ce4651b5aedaa2b25bb3d9",
       "stage": "Stage.SOMESTAGENAME",
       "progress": 0.3,     # could be fraction of one or percentage
    }
    """
    run_id = serializers.CharField(max_length=100)
    stage = serializers.CharField(max_length=100)
    progress = serializers.FloatField()


class ContentChannelSaveToProfileSerializer(serializers.Serializer):
    """
    A true/false single-field serializer for saving channel to profile.
    """
    save_channel_to_profile = serializers.BooleanField()

class ChannelControlSerializer(serializers.Serializer):
    """
    Handles POSTs of control commands.
    """
    command = serializers.CharField()
    options = serializers.JSONField()


