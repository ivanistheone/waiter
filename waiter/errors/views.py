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
        logfile_path = run.logfile.path
        run.logfile.open(mode='r')
        context['logs'] = run.logfile.readlines()
        for level in 'critical', 'error':
            try:
                with open("%s.%s" % (logfile_path, level)) as f:
                    context[level] = f.readlines()
            except OSError:
                context[level] = []
                continue
        return context