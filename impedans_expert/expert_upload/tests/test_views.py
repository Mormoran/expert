from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client
from django.contrib.auth import login, authenticate

from impedans_expert.expert_upload.models import FileUploadModel, FileType
from impedans_expert.users.models import User
from impedans_expert.expert.models import Customer
from .. views import FileUpload

# test the views
class UploadViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(name="test", username="test", password="testing1212")
        self.user.set_password("testing1212")
        self.user.save()

        self.customer = Customer.objects.create(company_name="TestCompany", contact_name="person",
                                contact_email="p.s@m.com", user=self.user)

    def test_url_accessibility(self):
        response = self.client.get('/expert_upload/file/add')
        self.assertEqual(response.status_code, 301)
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_by_name(self):
        self.client.login(username=self.user.username, password="testing1212")
        response = self.client.get(reverse('expert_upload:File_Upload-add'), follow=True)
        self.assertEqual(response.status_code, 200)
