
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
            print(log_file.read())
            log_contents = log_file.read()
            self.assertIn(log_contents, "UNIQUESTRING94913")

        self.assertTrue(run.channel == ch)
        self.assertTrue(run.channel.channel_id == ch.channel_id)

