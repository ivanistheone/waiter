
from django.test import TestCase

from runs.models import ContentChannel, ContentChannelRun, ChannelRunLog


class BasicModelsCreation(TestCase):
    
    def test_channel_run_file_creation(self):
        """
        MMMMMMVT for object creation and related fields work as expected.
        """
        ch = ContentChannel()
        ch.save()

        run = ContentChannelRun(channel=ch)
        run.save()

        # check ch.runs populated
        run_ids = [run.run_id for run in ch.runs.all()]
        self.assertTrue(run.run_id in run_ids)

        runlog = ChannelRunLog(run=run, logfile='name_that_will_be_ignored.log')
        runlog.save()

        # write something to logfile
        with open(runlog.logfile.path, 'w') as log_file:
            log_file.write('A test line UNIQUESTRING94913 added manually\n')

        # check if it workded
        with open(runlog.logfile.path, 'r') as log_file:
            print(log_file.read())
            log_contents = log_file.read()
            self.assertIn(log_contents, "UNIQUESTRING94913")
