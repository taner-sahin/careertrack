from django.test import TestCase
from django.urls import reverse
from .models import Company


class CompanyTests(TestCase):

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            website="https://www.testcompany.com",
            location="İstanbul",
            
        )

    def test_company_str(self):
        self.assertEqual(
            str(self.company),
            "Test Company",
        )
        
    def test_company_slug_created(self):
     self.assertIsNotNone(
        self.company.slug
    )

     self.assertEqual(
        self.company.slug,
        "test-company",
    )
     
    def test_company_list_view(self):
     response = self.client.get(
        reverse("companies:list")
    )

     self.assertEqual(
        response.status_code,
        200,
    )

     self.assertContains(
        response,
        "Test Company",
    )
    
    def test_company_detail_view(self):
     response = self.client.get(
        reverse(
            "companies:detail",
            kwargs={"slug": self.company.slug},
        )
    )

     self.assertEqual(
        response.status_code,
        200,
    )

     self.assertContains(
        response,
        "Test Company",
    )
     
    def test_company_create_view(self):
     response = self.client.post(
        reverse("companies:create"),
        {
            "name": "Microsoft",
            "website": "https://www.microsoft.com",
            "location": "USA",
        },
    )

     self.assertEqual(
        response.status_code,
        302,
    )

     self.assertTrue(
        Company.objects.filter(
            name="Microsoft"
        ).exists()
    )
     
    