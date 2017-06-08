from datetime import datetime, timedelta

from django.views.generic.base import TemplateView
from django.utils.safestring import mark_safe

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
        "run_status": kwargs.get('run_status', 'success')
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
            last_run = ContentChannelRun.objects.filter(channel__channel_id=channel.channel_id)[:1]
            context['inactive_channels'].append({
                    "channel": channel.name,
                    "channel_url": "%s/%s/edit" % (channel.default_content_server, channel.channel_id),
                    "restart_color": 'secondary',
                    "stop_color": "secondary",
                    "id": channel.channel_id,
                    "last_run": datetime.strftime("%b %w, %H:%M",last_run.events[-1].finished),
                    # do we have an overall event or do we have to sum these?
                    "duration": "0",
                    "status": last_run.events[-1].name,
                    # TODO
                    "status_pct": 100,
                    "num_errors": 0,
                    "run_status": "success",
                })

        context['jschannels'] = mark_safe(','.join("\"%s\"" % s for s in channel_names))
        return context