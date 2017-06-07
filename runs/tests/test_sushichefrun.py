"""
SushiChef event-reporing flow test suite.

More info:
http://www.django-rest-framework.org/api-guide/testing
https://docs.djangoproject.com/en/1.7/topics/testing/advanced/

"""
import uuid

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from runs.models import ContentChannel, ContentChannelRun, ChannelRunLog, ChannelRunEvent



class SushiChefFlowTest(APITestCase):

    def setUp(self):
        client = APIClient()


    def _create_test_content_channel(self):
        """
        Test registraction of a new content channel.
        """
        url = reverse('list_details')
        print('POST', url)
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
        print('POST', url)
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

    def test_create_run(self):
        """
        Test new run works.
        """
        self._create_test_content_channel()
        self._create_test_run()


    def test_create_run_events(self):
        """
        Test new run works.
        """
        self._create_test_content_channel()
        self._create_test_run()
        url = reverse('events_for_run', kwargs={'run_id': self._random_run_id})
        events = [
            {
                "run_id": self._random_run_id,
                "event": "STARTED",
                "progress": 0,
                "timestamp": "2017-06-07T04:44:49Z"
            },
            {
                "run_id": self._random_run_id,
                "event": "PROGRESSED",
                "progress": 0.3,
                "timestamp": "2017-06-07T04:47:05Z"
            },
            {
                "run_id": self._random_run_id,
                "event": "FINISHED",
                "progress": 1.0,
                "timestamp": "2017-06-07T04:49:05Z"
            }
        ]
        for event in events:
            print('POST', url)
            response = self.client.post(url, event, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Can't create event")        
            self.assertIsNotNone(response.data['id'], "event.id is missing")
            self.assertIsNotNone(response.data['run_id'], "run_id is missing")
        events_for_run_in_db = ChannelRunEvent.objects.filter(run_id=self._random_run_id)
        self.assertEqual(len(list(events_for_run_in_db)), 3, 'Wrong number of events in DB')




