
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ContentChannel, ContentChannelRun, ChannelRunLog, ChannelRunEvent
from .serializers import ContentChannelSerializer, ContentChannelCreateSerializer
from .serializers import ContentChannelRunSerializer, ContentChannelRunCreateSerializer

class ContentChannelList(APIView):
    """
    List all content channels or create a new channel.
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        """
        List all content channels.
        """
        channels = ContentChannel.objects.all()
        serializer = ContentChannelSerializer(channels, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Register a new content channels at the sushi bar.
        """
        serializer = ContentChannelCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentChannelDetail(APIView):
    """
    Retrieve, update, or delete a content channel instance.
    """
    def get_object(self, channel_id):
        try:
            return ContentChannel.objects.get(channel_id=channel_id)
        except ContentChannel.DoesNotExist:
            raise Http404

    def get(self, request, channel_id, format=None):
        channel = self.get_object(channel_id)
        serializer = ContentChannelSerializer(channel)
        return Response(serializer.data)

    def put(self, request, channel_id, format=None):
        channel = self.get_object(channel_id)
        serializer = ContentChannelSerializer(channel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, channel_id, format=None):
        channel = self.get_object(channel_id)
        channel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# CHANNEL RUNS #################################################################

class ContentChannelRunList(APIView):
    """
    List all runs for a given content channels.
    """
    def get(self, request, channel_id, format=None):
        """
        List all content channel runs.
        """
        channel = ContentChannel.objects.get(channel_id=channel_id)
        serializer = ContentChannelRunSerializer(channel.runs, many=True)
        return Response(serializer.data)

class ContentChannelRunCreate(APIView):
    """
    Create a new channel run.
    """
    def post(self, request, format=None):
        """
        Create a new channel run.
        """
        serializer = ContentChannelRunCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


