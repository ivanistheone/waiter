
from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ContentChannel, ContentChannelRun, ChannelRunLog, ChannelRunEvent
from .serializers import ContentChannelSerializer, ContentChannelRunSerializer, ChannelRunEventSerializer


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

    def put(self, request, run_id, format=None):
        run = self.get_object(run_id)
        serializer = ContentChannelRunSerializer(run, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, run_id, format=None):
        run = self.get_object(run_id)
        run.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# CHANNEL RUN EVENTS ###########################################################

class ChannelRunEventListCreate(APIView):
    """
    GET:  list all events for run `run_id`
    POST: create a new event for run `run_id`
    """
    def get(self, request, run_id, format=None):
        try:
            run = ContentChannelRun.objects.get(run_id=run_id)
        except ContentChannelRun.DoesNotExist:
            raise Http404
        serializer = ChannelRunEventSerializer(run.events, many=True)
        return Response(serializer.data)

    def post(self, request, run_id, format=None):
        """
        Create a new channel run.
        """
        serializer = ChannelRunEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
