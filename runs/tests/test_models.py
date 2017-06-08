
import os
import uuid

from django.test import TestCase

from runs.models import ContentChannel, ContentChannelRun, ChannelRunStage


class BasicModelsCreation(TestCase):
    
    def test_channel_run_file_creation(self):
        """
        MMMMMMVT for object creation and related fields work as expected.
        """
        random_uuid = uuid.uuid4()
        ch = ContentChannel(channel_id=random_uuid)
        ch.save()

        run = ContentChannelRun(channel=ch)
        run.save()

        # check ch.runs populated
        run_ids = [run.run_id for run in ch.runs.all()]
        self.assertTrue(run.run_id in run_ids)

        # write something to logfile
        with open(run.logfile.path, 'w') as log_file:
            log_file.write('A test line UNIQUESTRING94913 added manually\n')

        # check if it workded
        with open(run.logfile.path, 'r') as log_file:
            log_contents = log_file.read()
            self.assertIn("UNIQUESTRING94913", log_contents)

        self.assertTrue(run.channel == ch)
        self.assertTrue(run.channel.channel_id == ch.channel_id)
        self._cleanup_logfile_and_logdir(run.run_id)

    def test_logfile_created(self):
        random_uuid = uuid.uuid4()
        ch = ContentChannel(channel_id=random_uuid)
        ch.save()
        run = ContentChannelRun(channel=ch)
        run.save()
        self.assertIsNotNone(run.logfile)
        self.assertIsNotNone(run.logfile.path)
        self._cleanup_logfile_and_logdir(run.run_id)

    def test_logfile_not_overwritten_every_save(self):
        random_uuid = uuid.uuid4()
        ch = ContentChannel.objects.create(channel_id=random_uuid)
        run = ContentChannelRun.objects.create(channel=ch)
        self.assertIsNotNone(run.logfile)
        self.assertIsNotNone(run.logfile.path)
        # write something to logfile
        with open(run.logfile.path, 'w') as log_file:
            log_file.write('A test line UNIQUESTRING94813 added manually\n')
        # save
        run.started_by_user_token = 'changed'
        run.save()
        # check logfile persisted
        with open(run.logfile.path, 'r') as log_file:
            log_contents = log_file.read()
        self._cleanup_logfile_and_logdir(run.run_id)

    def _cleanup_logfile_and_logdir(self, test_run_id):
        run = ContentChannelRun.objects.get(run_id=test_run_id)
        logfile_path = run.logfile.path
        dirname, _ = channel_dir = os.path.split(logfile_path)
        os.remove(run.logfile.path)
        try:
            os.rmdir(dirname)
        except OSError:
            pass
