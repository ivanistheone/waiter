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

def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'T', suffix)

# Darjeeling Limited
progress_bar_colors = ["#FF0000", "#00A08A", "#F2AD00", "#F98400", "#5BBCD6", "#ECCBAE", "#046C9A", "#D69C4E", "#ABDDDE", "#000000"]
resource_icons = {".mp4": "fa-video-camera", ".png": "fa-file-image-o", ".pdf": "fa-file-pdf-o", ".zip": "fa-file-archive-o"}

format_duration = lambda t: str(timedelta(seconds=t.seconds))

class RunView(TemplateView):

    template_name = "runs.html"

    def get_context_data(self, **kwargs):
        context = super(RunView, self).get_context_data(**kwargs)
        run_id = uuid.UUID(kwargs.get('runid', ''))
        run = ContentChannelRun.objects.get(run_id=run_id)
        # TODO(arvnd): The previous run will be wrong for any run that 
        # is not the most recent.
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

        context['run_stats'] = []
        if run.resource_counts:
            for k, v in run.resource_counts.items():
                prev_value = previous_run.resource_counts.get(k, 0) if previous_run.resource_counts else 0
                bg_class = "table-default"
                if v < prev_value:
                    bg_class = "table-danger"
                elif v > prev_value:
                    bg_class = "table-success"
                context['run_stats'].append({
                        "icon": resource_icons.get(k, "fa-file"),
                        "name": k,
                        "value": v,
                        "previous_value": prev_value if prev_value else "-",
                        "bg_class": bg_class,
                    })

        if self.request.user in run.channel.followers.all():
            # closed star if the user has already saved this.
            context['saved_icon_class'] = 'fa-star'
        else:
            context['saved_icon_class'] = 'fa-star-o'

        # todo graphs
        # todo save to my profile

        return context