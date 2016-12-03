from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from ..api import views
from ..api import serializers
from .. import models


class JsonViewTests(TestCase):
    """ All pages should:

        1. Resolve to the proper View
        2. Return a 200 (login_required urls return 403 if not logged in)

    """
    fixtures = ['data/tests_auth_users.json']

    @classmethod
    def setUpClass(cls):
        super(JsonViewTests, cls).setUpClass()
        cls.factory = APIRequestFactory()
        cls.test_user = User.objects.filter(pk=1)

    def get_request(self, method='GET', authed=True):
        request_method = getattr(self.factory, method.lower())
        request = request_method("")
        if authed:
            force_authenticate(request, self.test_user.first())
        return request

    def test_jobs_collection_resolves(self):
        url = reverse('api_clean:job_collection',
                      args=[])
        view = resolve(url)
        self.assertEqual(view.func.__name__,
                         views.JobCollection.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_feedback_collection_resolves(self):
        url = reverse('api_clean:feedback_collection',
                      args=[])
        view = resolve(url)
        self.assertEqual(view.func.__name__,
                         views.FeedbackCollection.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_feedback_detail_resolves(self):
        url = reverse('api_clean:feedback_detail',
                      args=[1])
        view = resolve(url)
        self.assertEqual(view.func.__name__,
                         views.FeedbackDetail.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_feedback_level_collection_resolves(self):
        url = reverse('api_clean:feedback_level_collection',
                               args=[])
        view = resolve(url)
        self.assertEqual(view.func.__name__,
                         views.FeedbackLevelCollection.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_technician_collection_resolves(self):
        url = reverse('api_clean:technician_collection',
                      args=[])
        view = resolve(url)
        self.assertEqual(view.func.__name__,
                         views.TechnicianCollection.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_technician_detail_resolves(self):
        url = reverse('api_clean:technician_detail',
                      args=[1])
        view = resolve(url)
        self.assertEqual(view.func.__name__,
                         views.TechnicianDetail.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_uploadeddata_collection_resolves(self):
        url = reverse('api_clean:uploaded_data_collection',
                      args=[])
        view = resolve(url)
        self.assertEqual(view.func.__name__,
                         views.UploadedDataCollection.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)
        self.client.login(username='test_admin_user', password='razzle01')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)