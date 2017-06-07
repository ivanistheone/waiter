
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _


# Channel run states to recognized by the sushibar server
RUN_SCHEDULED = 'SCHEDULED'
RUN_CREATED = 'CREATED'
RUN_STARTED = 'STARTED'
RUN_RUNNING = 'RUNNING'
RUN_FINISHED = 'FINISHED'
RUN_ERROR = 'ERROR'
CHANNEL_RUN_STATES = (
    (RUN_SCHEDULED, 'Scheduled'),
    (RUN_CREATED, 'Created'),
    (RUN_STARTED, 'Started'),
    (RUN_RUNNING, 'Running'),
    (RUN_FINISHED, 'Finished'),
    (RUN_ERROR, 'Error'),
)

class LEUUIDField(models.CharField):
    """
    Custom field for storing UUIDs as strings.
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 32
        super(LEUUIDField, self).__init__(*args, **kwargs)

    def get_default(self):
        result = super(LEUUIDField, self).get_default()
        if isinstance(result, uuid.UUID):
            result = result.hex
        return result


class ContentChannel(models.Model):
    """
    The sushibar contect channel representation.
    """
    # id = local, implicit, autoincrementing integer primary key
    channel_id = LEUUIDField('The id from contentcuration.models.Channel')
    name = models.CharField(max_length=200, blank=True)  # equiv to ricecooker's `title`
    description = models.CharField(max_length=400, blank=True)
    version = models.IntegerField(default=0)
    source_domain = models.CharField(max_length=300, blank=True, null=True)
    source_id = models.CharField(max_length=200, blank=True, null=True)

    # User-related fields (the person who registered the channel with sushibar)
    user_registered_by = models.EmailField(max_length=200, blank=True, null=True)
    user_token = models.CharField(max_length=200, blank=True, null=True)

    # Content curation related fields
    content_server = models.URLField(max_length=300, default='https://develop.contentworkshop.learningequality.org')




class ContentChannelRun(models.Model):
    """
    A particular sushi chef run for the content channel `channel`.
    """
    run_id = LEUUIDField(primary_key=True, default=uuid.uuid4)
    channel = models.ForeignKey(ContentChannel, on_delete=models.CASCADE, related_name='runs')
    chef_name = models.CharField(max_length=200)
    ricecooker_version = models.CharField(max_length=100, blank=True, null=True)

    # Denormalized info extracted from run events table
    state = models.CharField(max_length=20, choices=CHANNEL_RUN_STATES, default=RUN_CREATED)
    started = models.DateTimeField(verbose_name=_("started"), blank=True, null=True)
    finished = models.DateTimeField(verbose_name=_("finished"), blank=True, null=True)
    duration = models.DurationField(verbose_name=_("duration"), blank=True, null=True)

    # Stats: we could store using Entity-Attribute-Value data model
    #   - Number of different content types
    #   - File size totals
    #   - Number of log type counts (error messages)
    #   - Errors
    #   - Store command-line toggles: --staging / --publish / --update



class ChannelRunEvent(models.Model):
    """
    Represents lifecycle events for a given channel run.
    """
    # id = local, implicit, autoincrementing integer primary key
    run = models.ForeignKey(ContentChannelRun, on_delete=models.CASCADE, related_name='events')
    event = models.CharField(max_length=100)
    progress = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField()



def log_filename_for_run(instance, filename):
    """
    Generate the log filename based on `channel_id` and `run_id`.
    """
    # Run logfile will be saved in MEDIA_ROOT/sushicheflogs/channel_id/run_id.log
    return 'sushicheflogs/{0}/{1}.log'.format(instance.run.channel.channel_id, instance.run.run_id)

class ChannelRunLog(models.Model):
    """
    Stores the log file for the content channel run `run`.
    """
    # id = local, implicit, autoincrementing integer primary key
    run = models.OneToOneField(ContentChannelRun, on_delete=models.CASCADE, related_name='runlog')
    logfile = models.FileField(upload_to=log_filename_for_run, verbose_name='Log file from the sushi chef run.')
