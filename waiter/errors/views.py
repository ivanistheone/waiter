import uuid
from datetime import datetime, timedelta

from django.views.generic.base import TemplateView
from django.utils.safestring import mark_safe

from runs.models import *

class RunErrorsView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(RunErrorsView, self).get_context_data(**kwargs)
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