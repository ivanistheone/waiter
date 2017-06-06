from django.conf.urls import url
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns

from .api import ContentChannelList


urlpatterns = [
    url(r'channels/$', ContentChannelList.as_view()),
    # url(r'^channels/(?P<channel_id>[0-9]+)/$', api.ContentChannelDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
