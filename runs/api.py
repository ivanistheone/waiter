
from datetime import timedelta

from django.http import Http404
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ContentChannel, ContentChannelRun, ChannelRunStage
from .serializers import ContentChannelSerializer
from .serializers import ContentChannelRunSerializer
from .serializers import ChannelRunStageCreateSerializer, ChannelRunStageSerializer
from .serializers import ChannelRunLogMessageCreateSerializer
from .serializers import ChannelRunProgressReceiveSerializer

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
    List and access the events associated with ContentChannelRun `run_id`.
    """
    def get(self, request, run_id, format=None):
        """
        List all stages for channel runs.
        """
        stages = ChannelRunStage.objects.all()
        serializer = ChannelRunStageSerializer(stages, many=True)
        return Response(serializer.data)

    def post(self, request, run_id, format=None):
        """
        POST: notify sushibar of a given sushichef event for `run_id`.
        """
        # print(request.data)
        create_serializer = ChannelRunStageCreateSerializer(data=request.data)
        if create_serializer.is_valid():
            # print(create_serializer.data)
            assert run_id == create_serializer.data['run_id'], 'run_id mismatch in HTTP POST'
            duration = timedelta(seconds=create_serializer.data['duration'])
            server_time = timezone.now()
            calculated_started = server_time - duration
            run_stage = ChannelRunStage.objects.create(run_id=run_id,
                                                       name=create_serializer.data['stage'],
                                                       started=calculated_started,
                                                       finished=server_time,
                                                       duration=duration)
            response_serializer = ChannelRunStageSerializer(run_stage)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CHANNEL RUN LOGS #############################################################

class ChannelRunLogMessageCreate(APIView):

    def post(self, request, run_id, format=None):
        """
        Append the log message to the logfile for the run `run_id`.
        """
        serializer = ChannelRunLogMessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            assert run_id == serializer.data['run_id'], 'run_id mismatch in HTTP POST'
            run = ContentChannelRun.objects.get(run_id=run_id)
            # datetime.utcfromtimestamp(serializer.data['created']) convert ???
            with open(run.logfile.path, 'a') as logfile:
                logfile.write(str(serializer.data['created'])+':\t'+serializer.data['message'] + '\n')
            return Response({'result':'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# CHANNEL RUN PROGRESS #########################################################

class ChannelRunProgressViews(APIView):

    def get(self, request, run_id, format=None):
        """
        Return current progress from redis.
        """
        print('Reading from redis...')
        # INSERT REDIS RETRIEVE CODE HERE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


        return Response({'progress':0.0})




    def post(self, request, run_id, format=None):
        """
        Store progress update to redis.
        """
        serializer = ChannelRunProgressReceiveSerializer(data=request.data)
        if serializer.is_valid():
            print('Storing to redis...')
            # here you can be sure that serializer.data is valid 
            # {
            #    "run_id": "f2c0906a77ce4651b5aedaa2b25bb3d9",
            #    "stage": "Stage.SOMESTAGENAME",
            #    "progress": 0.3,     # could be fraction of one or percentage
            # }
            print(serializer.data)
            # INSERT REDIS STORE CODE HERE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


            return Response({'result':'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

