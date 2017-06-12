from datetime import datetime, timedelta
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

def get_mock(**kwargs):
    return {
        "channel": kwargs.get('channel', 'Khan Academy'),
        "channel_url": kwargs.get('channel_url', 'https://contentworkshop.learningequality.org/channels/ac0de44904b751adb1eac16570b41184/edit'),
        "restart_color": kwargs.get('restart_color', 'success'),
        "stop_color": kwargs.get('stop_color', 'danger'),
        "id": kwargs.get('id', 1),
        "last_run": kwargs.get('last_run', "Jun 1, 1:24 PM"),
        "duration": kwargs.get('duration', "47:30"),
        "status": kwargs.get('status', 'Completed'),
        "status_pct": kwargs.get('status_pct', 100),
        "num_errors": kwargs.get('num_errors', 0),
        "run_status": kwargs.get('run_status', 'success'),
        "last_run_id": 1
    }

class DashboardView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['keys'] = ('Active Channels', 'Inactive Channels')
        channel_names = ['TESSA', 'Pratham', 'MIT', 'Khan Academy']
        context['channels'] = dict(zip(context['keys'], ([get_mock(), get_mock(channel='TESSA', restart_color='secondary'), get_mock(channel='Pratham', run_status='warning', num_errors=14), get_mock(channel='MIT', status_pct=50, status='Scraping')], [get_mock()])))
        # TODO(arvnd): This can very easily be optimized by
        # querying the runs table directly.
        for channel in ContentChannel.objects.all():
            # TODO(arvnd): add active bit to channel model and 
            # split on that.
            # TODO(arvnd): use .latest(created)
            last_run = channel.runs.all()[:1]
            if not len(last_run):
                print("No runs for channel %s " % channel.name)
                continue
            last_run = last_run[0]
            last_event = last_run.events.latest("finished")
            progress = REDIS.hgetall(last_run.run_id.hex)

            context['channels']['Inactive Channels'].append({
                    "channel": channel.name,
                    "channel_url": "%s/%s/edit" % (channel.default_content_server, channel.channel_id),
                    "restart_color": 'secondary',
                    "stop_color": "secondary",
                    "id": channel.channel_id,
                    "last_run": datetime.strftime(last_event.finished, "%b %w, %H:%M"),
                    "last_run_id": last_run.run_id,
                    # do we have an overall event or do we have to sum these?
                    "duration": "0",
                    "status": last_event.name.replace("Status.",""),
                    # TODO
                    "status_pct": progress.get('progress', 0) * 100 if progress else 0,
                    "num_errors": 0,
                    "run_status": "success",
                })

        context['jschannels'] = mark_safe(','.join("\"%s\"" % s for s in channel_names))
        return context