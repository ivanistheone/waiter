"""
SushiChef event-reporing flow test suite.

More info:
http://www.django-rest-framework.org/api-guide/testing
https://docs.djangoproject.com/en/1.7/topics/testing/advanced/

"""
import os
import uuid
from datetime import datetime

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from runs.models import ContentChannel, ContentChannelRun, ChannelRunStage



class SushiChefFlowTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def _create_test_content_channel(self):
        """
        Test registraction of a new content channel.
        """
        url = reverse('list_details')
        self._random_uuid = uuid.uuid4()
        channel_data = {
            "channel_id": self._random_uuid,
            "name": "Chennel name slash title (EN)",
            "description": "A test channel",
            "version": 3,
            "source_domain": "learningequality.org",
            "source_id": "The test channel v0.1",
            "user_registered_by": "content@learningequality.org",
            "user_token": "a92a8ff947c8423ed0cd11c6ce33ad6b95b65633",
            "content_server": "https://develop.contentworkshop.learningequality.org"
        }
        response = self.client.post(url, channel_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Can't register content channel")

    def test_create_content_channel(self):
        """
        Test registraction of a new content channel.
        """
        self._create_test_content_channel()


    def _create_test_run(self):
        """
        Creates a run for the test content channel.
        
        depends on: _create_test_content_channel
        """
        url = reverse('list_runs')
        run_data = {
            "channel_id": self._random_uuid,
            "chef_name": "le-chef-name",
            "ricecooker_version": "0.4"
        }
        response = self.client.post(url, run_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Can't start run")
        self.assertIsNotNone(response.data['run_id'], "run_id missing")
        self._random_run_id = response.data['run_id']
        self.assertEqual(response.data['channel']['channel_id'], self._random_uuid.hex , "Wrong channel rel'n")

    def _cleanup_logfile_and_logdir(self):
        run = ContentChannelRun.objects.get(run_id=self._random_run_id)
        logfile_path = run.logfile.path
        channel_dir, _ =  os.path.split(logfile_path)
        os.remove(run.logfile.path)
        os.rmdir(channel_dir)

    def test_create_run(self):
        """
        Test new run works.
        """
        self._create_test_content_channel()
        self._create_test_run()
        self._cleanup_logfile_and_logdir()


    def test_create_run_and_stages(self):
        """
        Test run stage reporting works.
        """
        self._create_test_content_channel()
        self._create_test_run()
        url = reverse('list_run_stages', kwargs={'run_id': self._random_run_id})
        stages_notify_posts = [
            {
                "run_id": self._random_run_id,
                "stage": "Stage.STARTED",
                "duration": 0,
            },
            {
                "run_id": self._random_run_id,
                "stage": "Stage.PROGRESSED",
                "duration": 1000,
            },
            {
                "run_id": self._random_run_id,
                "stage": "Stage.FINISHED",
                "duration": 5000,
            }
        ]
        for stage_post in stages_notify_posts:
            response = self.client.post(url, stage_post, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Can't create event")        
            self.assertIsNotNone(response.data['started'], "started missing")
            self.assertIsNotNone(response.data['finished'], "finished is missing")
            self.assertEqual(response.data['duration'], stage_post['duration'], "wrong duration")
            # self.assertEqual(response.data['run_id'],  self._random_run_id, "wrong run_id")
        
        # check API returns correct
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), len(stages_notify_posts), "wrong number of stages")

        # check DB agrees
        stages_for_run_in_db = ChannelRunStage.objects.filter(run_id=self._random_run_id)
        self.assertEqual(len(list(stages_for_run_in_db)), len(stages_notify_posts), 'Wrong number of stages in DB')
        self._cleanup_logfile_and_logdir()


    def test_create_run_and_log_messages(self):
        """
        Test run log messages are written to disk.
        """
        self._create_test_content_channel()
        self._create_test_run()
        url = reverse('create_run_log_message', kwargs={'run_id': self._random_run_id})
        log_message_posts = [
            {
                "run_id": self._random_run_id,
                'created': datetime.now().timestamp(),
                'message': 'LOG MESSAGE 1013913'
            },
            {
                "run_id": self._random_run_id,
                'created': datetime.now().timestamp(),
                'message': 'LOG MESSAGE progressing'
            },
            {
                "run_id": self._random_run_id,
                'created': datetime.now().timestamp(),
                'message': 'LOG MESSAGE 19929294'
            }
        ]
        for log_message_post in log_message_posts:
            response = self.client.post(url, log_message_post, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Can't create event")
            self.assertEqual(response.data['result'], 'success', "logging message not successful")

        # check log messages exist
        run = ContentChannelRun.objects.get(run_id=self._random_run_id)
        with open(run.logfile.path, 'r') as logfile:
            log_contents = logfile.read()
            for log_message_post in log_message_posts:
                self.assertIn(log_message_post['message'], log_contents)

        self._cleanup_logfile_and_logdir()

