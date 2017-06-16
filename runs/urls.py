from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .api import ContentChannelListCreate, ContentChannelDetail, RunsForContentChannelList
from .api import ContentChannelRunListCreate, ContentChannelRunDetail
from .api import ChannelRunStageListCreate
from .api import ChannelRunProgressEndpoints
from .api import ContentChannelSaveToProfile
from .api import ChannelControlEndpoints

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
    url(regex=r'channels/(?P<channel_id>[0-9A-Fa-f-]+)/save_to_profile/$',
        view=ContentChannelSaveToProfile.as_view(),
        name='save_channel_to_profile'),
    #
    url(regex=r'channels/(?P<channel_id>[0-9A-Fa-f-]+)/control/$',
        view=ChannelControlEndpoints.as_view(),
        name='channel_control'),
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
        view=ChannelRunStageListCreate.as_view(),
        name='list_run_stages'),
    #
    url(regex=r'channelruns/(?P<run_id>[0-9A-Fa-f-]+)/progress/$',
        view=ChannelRunProgressEndpoints.as_view(),
        name='run_progress'),
]



urlpatterns = format_suffix_patterns(urlpatterns)
