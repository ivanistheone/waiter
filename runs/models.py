
from io import StringIO
import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _

__all__ = ["ContentChannel", "ContentChannelRun", "ChannelRunStage"]

class ContentChannel(models.Model):
    """
    The sushibar contect channel representation.
    """
    # id = local, implicit, autoincrementing integer primary key
    channel_id = models.UUIDField('The id from contentcuration.models.Channel')
    name = models.CharField(max_length=200, blank=True)  # equiv to ricecooker's `title`
    description = models.CharField(max_length=400, blank=True)
    version = models.IntegerField(default=0)
    source_domain = models.CharField(max_length=300, blank=True, null=True)
    source_id = models.CharField(max_length=200, blank=True, null=True)

    # Authorization-related fields for channel (not used in MMVP)
    registered_by_user = models.EmailField(max_length=200, blank=True, null=True)
    registered_by_user_token = models.CharField(max_length=200, blank=True, null=True)
    default_content_server = models.URLField(max_length=300, default=settings.DEFAULT_CONTENT_CURATION_SERVER)

    def __str__(self):
        return '<Channel ' + self.channel_id.hex[:8] + '...>'



def log_filename_for_run(run, filename):
    """Generate the log filename based on `channel_id` and `run_id`."""
    # Run logfile will be saved in MEDIA_ROOT/sushicheflogs/channel_id/run_id.log
    return 'sushicheflogs/{0}/{1}.log'.format(run.channel.channel_id.hex, run.run_id.hex)

def create_empty_logfile(sender, **kwargs):
    """Create an empty logfile for the ContentChannelRun after its inital save."""
    run_instance = kwargs["instance"]
    if kwargs["created"]:
        dummy_file = StringIO()
        run_instance.logfile.save('dummy_filename.log', dummy_file)

class ContentChannelRun(models.Model):
    """
    A particular sushi chef run for the content channel `channel`.
    """
    run_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel = models.ForeignKey(ContentChannel, on_delete=models.CASCADE, related_name='runs')
    chef_name = models.CharField(max_length=200)
    ricecooker_version = models.CharField(max_length=100, blank=True, null=True)
    logfile = models.FileField(upload_to=log_filename_for_run, blank=True, null=True)

    # Channel stats
    resource_counts = JSONField(blank=True, null=True)
    resource_sizes = JSONField(blank=True, null=True)

    # Extra optional attributes like error counts, and command-line toggles (--staging / --publish / --update)
    extra_options = JSONField(blank=True, null=True)

    # Authorization fields
    started_by_user = models.EmailField(max_length=200, blank=True, null=True)
    started_by_user_token = models.CharField(max_length=200, blank=True, null=True)
    content_server = models.URLField(max_length=300, default=settings.DEFAULT_CONTENT_CURATION_SERVER)

    def __str__(self):
        return '<Run ' + self.run_id.hex[:8] + '...>'

post_save.connect(create_empty_logfile, sender=ContentChannelRun, dispatch_uid="logfilefix")



class ChannelRunStage(models.Model):
    """
    Represents different stages of the given channel run.
    """
    # id = local, implicit, autoincrementing integer primary key
    run = models.ForeignKey(ContentChannelRun, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=100)    
    started = models.DateTimeField(verbose_name=_("started"), blank=True, null=True)
    finished = models.DateTimeField(verbose_name=_("finished"), blank=True, null=True)
    duration = models.DurationField(verbose_name=_("duration"), blank=True, null=True)

    def get_duration_in_seconds(self):
       return self.duration.total_seconds()

    def __str__(self):
        return '<RunStage for run ' + self.run.run_id.hex[:8] + '...>'
