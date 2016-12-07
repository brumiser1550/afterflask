from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .. import models


class UploadedDataTestCase(TestCase):
    fixtures = ['data/tests_auth_users.json',
                'data/tests_FeedbackLevel.json']

    def setUp(self):
        pass

    # struggling to get this to work, testing through the api instead
    # def test_save(self):
    #     """Verifying save works with both sheets."""
    #     user = User.objects.filter(email='fake@totallyfake.com').first()
    #     f = open('clean/fixtures/data/tests_Sheet1.csv', 'r')
    #     sheet1_data = SimpleUploadedFile('Sheet1.csv',
    #                                      f.read())
    #     sheet1 = models.UploadedData.objects.create(uploaded_by=user,
    #                                                 data=sheet1_data,
    #                                                 file_type='S1')
    #     sheet1.save()





