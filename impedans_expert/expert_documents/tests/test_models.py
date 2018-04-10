import os.path
from django.test import TestCase
from impedans_expert.expert_documents.models import DocumentUpload
from impedans_expert.users.models import User
from impedans_expert.expert.models import Customer
# test the views

class DocumentViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # do set up
        User.objects.create(name="Test", username="Test", password="testing1212")
        user = User.objects.get(name="Test")
        Customer.objects.create(company_name="TestCompany", contact_name="person",
                                contact_email="p.s@m.com", user=user)
        customer = Customer.objects.get(company_name="TestCompany")
        file = os.path.realpath("/home/luke/Downloads/build.txt")
        DocumentUpload.objects.create(file=file, _file_size=6,
                                      name="testdoc", owner=user, customer=customer)

        # def setUp(self):
        # do set up per method
        #    print("set up done")

    def test_document_name(self):
        # check doc
        doc = DocumentUpload.objects.get(id=1)
        self.assertEquals(doc.name, "testdoc")
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_document_owner(self):
        # check doc
        doc = DocumentUpload.objects.get(id=1)
        user = User.objects.get(name="Test")
        self.assertEquals(doc.owner, user)
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_document_customer(self):
        # check doc
        doc = DocumentUpload.objects.get(id=1)
        customer = Customer.objects.get(company_name="TestCompany")
        self.assertEquals(doc.customer, customer)
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

