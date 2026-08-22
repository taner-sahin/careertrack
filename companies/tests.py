from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Company


User = get_user_model()


class CompanyTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPass123!",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="OtherPass123!",
        )

        self.client.login(
            username="testuser",
            password="TestPass123!",
        )

        self.company = Company.objects.create(
            user=self.user,
            name="Test Company",
            website="https://www.testcompany.com",
            location="İstanbul",
        )

        self.other_company = Company.objects.create(
            user=self.other_user,
            name="Other Company",
            website="https://www.othercompany.com",
            location="Ankara",
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

        self.assertNotContains(
            response,
            "Other Company",
        )

    def test_company_detail_view(self):
        response = self.client.get(
            reverse(
                "companies:detail",
                kwargs={
                    "slug": self.company.slug,
                },
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

        company = Company.objects.get(
            name="Microsoft"
        )

        self.assertEqual(
            company.user,
            self.user,
        )

    def test_company_update_view(self):
        response = self.client.post(
            reverse(
                "companies:update",
                kwargs={
                    "slug": self.company.slug,
                },
            ),
            {
                "name": "Updated Company",
                "website": "https://updatedcompany.com",
                "location": "Ankara",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.company.refresh_from_db()

        self.assertEqual(
            self.company.name,
            "Updated Company",
        )

    def test_company_delete_view(self):
        response = self.client.post(
            reverse(
                "companies:delete",
                kwargs={
                    "slug": self.company.slug,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertFalse(
            Company.objects.filter(
                id=self.company.id,
            ).exists()
        )

    def test_other_user_company_detail_returns_404(self):
        response = self.client.get(
            reverse(
                "companies:detail",
                kwargs={
                    "slug": self.other_company.slug,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_other_user_company_update_returns_404(self):
        response = self.client.get(
            reverse(
                "companies:update",
                kwargs={
                    "slug": self.other_company.slug,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_other_user_company_delete_returns_404(self):
        response = self.client.get(
            reverse(
                "companies:delete",
                kwargs={
                    "slug": self.other_company.slug,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_company_views_require_login(self):
        self.client.logout()

        response = self.client.get(
            reverse("companies:list")
        )

        self.assertEqual(
            response.status_code,
            302,
        )