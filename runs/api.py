
from datetime import timedelta
import json

from django.conf import settings
from django.http import Http404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from channels import Group

from .models import ContentChannel, ContentChannelRun, ChannelRunStage
from .serializers import ContentChannelSerializer
from .serializers import ContentChannelRunSerializer
from .serializers import ChannelRunStageCreateSerializer, ChannelRunStageSerializer
from .serializers import ChannelRunProgressSerializer
from .serializers import ContentChannelSaveToProfileSerializer
from .serializers import ChannelControlSerializer

# REDIS connection #############################################################
import redis
REDIS = redis.StrictRedis(host=settings.MMVP_REDIS_HOST,
                          port=settings.MMVP_REDIS_PORT,
                          db=settings.MMVP_REDIS_DB,
                          charset="utf-8",
                          decode_responses=True)



# CONTENT CHANNELS #############################################################

class ContentChannelListCreate(ListCreateAPIView):
    """
    List all content channels or create a new channel.
    """
    queryset = ContentChannel.objects.all()
    serializer_class = ContentChannelSerializer

class ContentChannelDetail(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a content channel instance.
    """
    queryset = ContentChannel.objects.all()
    serializer_class = ContentChannelSerializer
    lookup_field =  'channel_id'

class ContentChannelSaveToProfile(APIView):
    """
    Save a content channel to the user profile.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, channel_id, format=None):
        """
        Handle "save to profile" ajax calls.
        """
        try:
            channel = ContentChannel.objects.get(channel_id=channel_id)
        except ContentChannel.DoesNotExist:
            raise Http404
        serializer = ContentChannelSaveToProfileSerializer(data=request.data)
        if serializer.is_valid():
            wants_saved = serializer.data['save_channel_to_profile']
            channel_followers = channel.followers.all()
            if wants_saved and request.user not in channel_followers:
                channel.followers.add(request.user)
                channel.save()
            if not wants_saved and request.user in channel_followers:
                channel.followers.remove(request.user)
                channel.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CHANNEL RUNS #################################################################

class RunsForContentChannelList(APIView):
    """
    List all runs for a given content channels.
    """
    def get(self, request, channel_id, format=None):
        """
        List all runs for content channel `channel_id`.
        """
        try:
            channel = ContentChannel.objects.get(channel_id=channel_id)
        except ContentChannel.DoesNotExist:
            raise Http404
        serializer = ContentChannelRunSerializer(channel.runs, many=True)
        return Response(serializer.data)

class ContentChannelRunListCreate(APIView):
    """
    Create a new channel run or list all channel runs.
    """
    def get(self, request, format=None):
        """
        List all content channel runs.
        """
        runs = ContentChannelRun.objects.all()
        serializer = ContentChannelRunSerializer(runs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create a new channel run.
        """
        serializer = ContentChannelRunSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContentChannelRunDetail(APIView):
    """
    Retrieve, update, or delete the data associated with a channel run.
    """
    def get_object(self, run_id):
        try:
            return ContentChannelRun.objects.get(run_id=run_id)
        except ContentChannelRun.DoesNotExist:
            raise Http404

    def get(self, request, run_id, format=None):
        run = self.get_object(run_id)
        serializer = ContentChannelRunSerializer(run)
        return Response(serializer.data)

    def patch(self, request, run_id, format=None):
        run = self.get_object(run_id)
        serializer = ContentChannelRunSerializer(run, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, run_id, format=None):
        run = self.get_object(run_id)
        run.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# CHANNEL RUN STAGES ###########################################################

class ChannelRunStageListCreate(APIView):
    """
    List and create the stages for the ContentChannelRun `run_id`.
    """
    def get(self, request, run_id, format=None):
        """
        List all stages for a channel run.
        """
        try:
            run = ContentChannelRun.objects.get(run_id=run_id)
        except ContentChannelRun.DoesNotExist:
            raise Http404
        stages = ChannelRunStage.objects.filter(run=run)
        serializer = ChannelRunStageSerializer(stages, many=True)
        return Response(serializer.data)

    def post(self, request, run_id, format=None):
        """
        POST: notify sushibar that `run_id` sushichef has finished a stage.
        """
        create_serializer = ChannelRunStageCreateSerializer(data=request.data)
        if create_serializer.is_valid():
            assert run_id == create_serializer.data['run_id'], 'run_id mismatch in HTTP POST'
            duration = timedelta(seconds=create_serializer.data['duration'])
            server_time = timezone.now()
            calculated_started = server_time - duration
            run_stage = ChannelRunStage.objects.create(run_id=run_id,
                                                       name=create_serializer.data['stage'],
                                                       started=calculated_started,
                                                       finished=server_time,
                                                       duration=duration)
            # TODO: cleanup dict in redis under name `run_id` on FINISHED stage
            response_serializer = ChannelRunStageSerializer(run_stage)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CHANNEL RUN PROGRESS #########################################################
# Temporary hack for MMVP --- manually store/retrieve progress in redis
# TODO: repalce with channels implementation for final version

class ChannelRunProgressEndpoints(APIView):

    def get(self, request, run_id, format=None):
        """
        Return current progress from redis.
        """
        progress_data_dict = REDIS.hgetall(run_id)
        serializer = ChannelRunProgressSerializer(progress_data_dict)
        return Response(serializer.data)

    def post(self, request, run_id, format=None):
        """
        Store progress update to redis.
        """
        serializer = ChannelRunProgressSerializer(data=request.data)
        if serializer.is_valid():
            REDIS.hmset(run_id, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ChannelControlEndpoints(APIView):

    def post(self, request, channel_id, format=None):
        """
        Store progress update to redis.
        """
        serializer = ChannelControlSerializer(data=request.data)
        if serializer.is_valid():
            print('Received command from frontend', serializer.data)
            group = Group('control-' + channel_id)
            msg_dict = dict(
                command=serializer.data['command'],
                options=serializer.data['options']
            )
            msg_text = json.dumps(msg_dict)
            print('Sending', msg_text, 'to group', group.name)
            group.send({'text': msg_text})
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

