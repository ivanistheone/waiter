from django.conf.urls import url
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns

from .api import ContentChannelListCreate, ContentChannelDetail, RunsForContentChannelList
from .api import ContentChannelRunListCreate, ContentChannelRunDetail
from .api import ChannelRunStageCreate

urlpatterns = [
    url(regex=r'channels/$',
        view=ContentChannelListCreate.as_view(),
        name='list_details'),
    #
    url(regex=r'channels/(?P<channel_id>[0-9A-Fa-f-]+)/$',
        view=ContentChannelDetail.as_view(),
        name='channel_details'),
    #
    url(regex=r'channels/(?P<channel_id>[0-9A-Fa-f-]+)/runs/$',
        view=RunsForContentChannelList.as_view(),
        name='runs_for_channel'),
    #
    #
    url(regex=r'channelruns/$',
        view=ContentChannelRunListCreate.as_view(),
        name='list_runs'),
    #
    url(regex=r'channelruns/(?P<run_id>[0-9A-Fa-f-]+)/$',
        view=ContentChannelRunDetail.as_view(),
        name='run_details'),
    #
    url(regex=r'channelruns/(?P<run_id>[0-9A-Fa-f-]+)/stages/$',
        view=ChannelRunStageCreate.as_view(),
        name='run_stage_notify'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
