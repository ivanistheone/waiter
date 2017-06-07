from django.conf.urls import url
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns

from .api import ContentChannelList, ContentChannelDetail
from .api import ContentChannelRunList, ContentChannelRunCreate


urlpatterns = [
    url(r'channels/$', ContentChannelList.as_view()),
    url(r'channels/(?P<channel_id>[0-9A-Fa-f-]+)/$', ContentChannelDetail.as_view()),
    url(r'channels/(?P<channel_id>[0-9A-Fa-f-]+)/runs/$', ContentChannelRunList.as_view()),
    url(r'channelruns/$', ContentChannelRunCreate.as_view()),
    # url(r'channelruns/(?P<run_id>[0-9A-Fa-f-]+)/$', ContentChannelRunDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
