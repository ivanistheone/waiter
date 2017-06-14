from datetime import datetime, timedelta, timezone
from django.conf import settings

from django.views.generic.base import TemplateView
from django.utils.safestring import mark_safe

from runs.models import *

import redis
# TODO(arvnd): Should probably get the redis adapter from some common
# place.
REDIS = redis.StrictRedis(host=settings.MMVP_REDIS_HOST,
                          port=settings.MMVP_REDIS_PORT,
                          db=settings.MMVP_REDIS_DB,
                          charset="utf-8",
                          decode_responses=True)

def get_status_pct(progress, failed):
    fmt_pct = lambda f: int(float(f) * 100)
    if failed:
        return 100
    if progress is None:
        return 0
    return fmt_pct(progress.get('progress', 0))

class DashboardView(TemplateView):

    template_name = "pages/home.html"
    view_saved = False

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['channels'] = {
            'Active Channels': [],
            'Inactive Channels': []
        }
        # TODO(arvnd): This can very easily be optimized by
        # querying the runs table directly.
        queryset = self.request.user.saved_channels if self.view_saved else ContentChannel.objects
        for channel in queryset.all():
            # TODO(arvnd): add active bit to channel model and 
            # split on that.
            try:
                last_run = channel.runs.latest("created_at")
            except ContentChannelRun.DoesNotExist:
                print("No runs for channel %s " % channel.name)
                continue
        
            try:
                last_event = last_run.events.latest("finished")
            except ChannelRunStage.DoesNotExist:
                print("No stages for run %s" % last_run.run_id.hex)
                continue

            progress = REDIS.hgetall(last_run.run_id.hex)
            total_duration = sum((event.duration for event in last_run.events.all()), timedelta())

            failed = any('fail' in x.name.lower() for x in last_run.events.all())

            context['channels']['Inactive Channels'].append({
                    "channel": channel.name,
                    "channel_url": "%s/%s/edit" % (channel.default_content_server, channel.channel_id),
                    "restart_color": 'secondary',
                    "stop_color": "secondary",
                    "id": channel.channel_id,
                    "last_run": datetime.strftime(last_event.finished, "%b %d, %H:%M"),
                    "last_run_id": last_run.run_id,
                    "duration": str(timedelta(seconds=total_duration.seconds)),
                    "status": "Failed" if failed else last_event.name.replace("Status.",""),
                    "status_pct": get_status_pct(progress, failed),
                    "run_status": "danger" if failed else "success",
                })

        return context