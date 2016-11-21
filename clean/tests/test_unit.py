from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User
from .. import views


class PageTest(TestCase):
    """ All pages should:

        1. Resolve to the proper View
        2. Return a 200 (login_required urls return 302 if not logged in)
        3. Use the appropriate template
        4. Contain the proper context data
    """
    fixtures = ['data/tests_auth_users.json']

    def test_company_page(self):
        """
        Test the company url and view
        """
        url = reverse('clean:company')
        v = resolve(url)
        self.assertEqual(v.func.__name__, views.CompanyView.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'clean/company.html')

    def test_leave_feedback_page(self):
        """
        Test the leave-feedback url and view
        """
        url = reverse('clean:leave-feedback')
        v = resolve(url)
        self.assertEqual(v.func.__name__, views.LeaveFeedbackView.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'clean/feedback.html')

    def test_technician_list_page(self):
        """
        Test the technicians url and view
        """
        url = reverse('clean:technicians')
        v = resolve(url)
        self.assertEqual(v.func.__name__, views.TechnicianListView.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.client.login(username='test_admin_user', password='razzle01')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'clean/technicians_list.html')

    def test_technician_detail_page(self):
        """
        Test the technicians detail url and view
        """
        url = reverse('clean:technician', args=[1])
        v = resolve(url)
        self.assertEqual(v.func.__name__, views.TechnicianDetailView.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.client.login(username='test_admin_user', password='razzle01')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'clean/technicians_detail.html')

    def test_job_list_page(self):
        """
        Test the job list url and view
        """
        url = reverse('clean:jobs')
        v = resolve(url)
        self.assertEqual(v.func.__name__, views.JobListView.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.client.login(username='test_admin_user', password='razzle01')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'clean/jobs_list.html')

    def test_job_detail_page(self):
        """
        Test the job detail url and view
        """
        url = reverse('clean:job', args=[1])
        v = resolve(url)
        self.assertEqual(v.func.__name__, views.JobDetailView.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.client.login(username='test_admin_user', password='razzle01')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'clean/jobs_detail.html')

    def test_feedback_list_page(self):
        """
        Test the feedback list url and view
        """
        url = reverse('clean:feedbacks')
        v = resolve(url)
        self.assertEqual(v.func.__name__, views.FeedbackListView.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.client.login(username='test_admin_user', password='razzle01')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'clean/feedback_list.html')

    def test_feedback_detail_page(self):
        """
        Test the feedback detail url and view
        """
        url = reverse('clean:feedback', args=[1])
        v = resolve(url)
        self.assertEqual(v.func.__name__, views.FeedbackDetailView.__name__)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.client.login(username='test_admin_user', password='razzle01')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'clean/feedback_detail.html')