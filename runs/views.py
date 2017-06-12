import uuid
from datetime import timedelta
from datetime import time

from django.conf import settings

from django.views.generic.base import TemplateView
from django.utils.safestring import mark_safe

from .models import *

import redis
# TODO(arvnd): Should probably get the redis adapter from some common
# place.
REDIS = redis.StrictRedis(host=settings.MMVP_REDIS_HOST,
                          port=settings.MMVP_REDIS_PORT,
                          db=settings.MMVP_REDIS_DB,
                          charset="utf-8",
                          decode_responses=True)

# Darjeeling Limited
progress_bar_colors = ["#FF0000", "#00A08A", "#F2AD00", "#F98400", "#5BBCD6", "#ECCBAE", "#046C9A", "#D69C4E", "#ABDDDE", "#000000"]

format_duration = lambda t: time(0, 0, t.seconds).strftime("%M:%S")

class RunView(TemplateView):

    template_name = "runs.html"

    def get_context_data(self, **kwargs):
        context = super(RunView, self).get_context_data(**kwargs)
        run_id = uuid.UUID(kwargs.get('runid', ''))
        run = ContentChannelRun.objects.get(run_id=run_id)
        # TODO(arvnd): This can very easily be optimized by
        # querying the runs table directly.
        previous_run = run.channel.runs.all()[:2]
        if len(previous_run) < 2:
            previous_run = None
        else:
            previous_run = previous_run[1]
        context['channel'] = run.channel
        context['run_stages'] = []
        total_time = timedelta()
        for idx, stage in enumerate(run.events.order_by('finished').all()):
            context['run_stages'].append({
                "duration": stage.duration,
                "name": stage.name.replace("Status.",""),
                "color": progress_bar_colors[idx % len(progress_bar_colors)]})
            total_time += stage.duration
        for stage in context['run_stages']:
            stage['percentage'] = stage['duration'] / total_time * 100
            stage['duration'] = format_duration(stage['duration'])
        context['total_time'] = format_duration(total_time)

        # todo resource counts
        # todo graphs
        # todo save to my profile

        return context