
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ContentChannel, ContentChannelRun, RunLogFile, ChannelRunEvent
from .serializers import ContentChannelSerializer, ContentChannelCreateSerializer


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
