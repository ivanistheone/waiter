import uuid
from datetime import datetime, timedelta

from django.views.generic.base import TemplateView
from django.utils.safestring import mark_safe

from runs.models import *

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

class RunErrorsView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(RunErrorsView, self).get_context_data(**kwargs)
        context['keys'] = ('Active Channels', 'Inactive Channels')
        channel_names = ['TESSA', 'Pratham', 'MIT', 'Khan Academy']
        context['channels'] = dict(zip(context['keys'], ([get_mock(), get_mock(channel='TESSA', restart_color='secondary'), get_mock(channel='Pratham', run_status='warning', num_errors=14), get_mock(channel='MIT', status_pct=50, status='Scraping')], [get_mock()])))

        run_id = uuid.UUID(kwargs.get('runid', ''))
        run = ContentChannelRun.objects.get(run_id=run_id)
        # Depending on how big these are, it's probably bad to 
        # load them in memory, we can use some file embed on S3, or 
        # at minimum track a static folder and have the client side 
        # load it.
        run.logfile.open(mode='r')
        log_string = run.logfile.read()
        context['logs'] = log_string.replace('\n', '<br>')
        return context