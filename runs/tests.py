
from django.test import TestCase

from runs.models import ContentChannel, ContentChannelRun, RunLogFile


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
        run_ids = [run.id for run in ch.runs.all()]
        self.assertTrue(run.id in run_ids)

        rlf = RunLogFile(run=run, logfile='name_that_will_be_ignored.log')
        rlf.save()

        # write something to logfile
        with open(rlf.logfile.path, 'w') as log_file:
            log_file.write('A test line UNIQUESTRING94913 added manually\n')

        # check if it workded
        with open(rlf.logfile.path, 'r') as log_file:
            print(log_file.read())
            log_contents = log_file.read()
            self.assertIn(log_contents, "UNIQUESTRING94913")
