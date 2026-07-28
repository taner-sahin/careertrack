from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase

from companies.models import Company
from .models import Application


class ApplicationModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )

        self.company = Company.objects.create(
            name="Test Company",
            website="https://example.com",
        )

        self.application = Application.objects.create(
            user=self.user,
            company=self.company,
            position="Django Backend Developer",
            status="applied",
        )

    def test_application_str(self):
        self.assertEqual(
            str(self.application),
            "Test Company - Django Backend Developer",
        )
        
    def test_application_list_view(self):
     self.client.login(
        username="testuser",
        password="testpass123",
    )

     response = self.client.get(
        reverse("applications:list")
    )

     self.assertEqual(response.status_code, 200)
     self.assertContains(response, "Django Backend Developer")
     
    def test_application_list_requires_login(self):
     response = self.client.get(
        reverse("applications:list")
    )

     self.assertEqual(response.status_code, 302)
     
    def test_application_detail_view(self):
     self.client.login(
        username="testuser",
        password="testpass123",
    )

     response = self.client.get(
        reverse(
            "applications:detail",
            kwargs={"slug": self.application.slug},
        )
    )

     self.assertEqual(response.status_code, 200)
     self.assertContains(
        response,
        "Django Backend Developer",
    )
     
    def test_application_update_view(self):
     self.client.login(
        username="testuser",
        password="testpass123",
    )

     response = self.client.post(
        reverse(
            "applications:update",
            kwargs={"slug": self.application.slug},
        ),
        {
            "company": self.company.id,
            "position": "Senior Django Developer",
            "status": "interview",
            "application_date": self.application.application_date,
            "notes": "Updated notes",
        },
    )

     self.assertEqual(response.status_code, 302)

     self.application.refresh_from_db()

     self.assertEqual(
        self.application.position,
        "Senior Django Developer",
    )
    
    def test_application_delete_view(self):
     self.client.login(
        username="testuser",
        password="testpass123",
    )

     response = self.client.post(
        reverse(
            "applications:delete",
            kwargs={"slug": self.application.slug},
        )
    )

     self.assertEqual(response.status_code, 302)

     self.assertFalse(
        Application.objects.filter(
            id=self.application.id
        ).exists()
    )
     
    def test_application_create_view(self):
     self.client.login(
        username="testuser",
        password="testpass123",
    )

     response = self.client.post(
        reverse("applications:create"),
        {
            "company": self.company.id,
            "position": "Python Backend Developer",
            "status": "applied",
            "application_date": self.application.application_date,
            "notes": "New application test",
        },
    )

     self.assertEqual(response.status_code, 302)

     self.assertTrue(
        Application.objects.filter(
            user=self.user,
            position="Python Backend Developer",
        ).exists()
    )
     
    def test_user_cannot_access_other_users_application(self):
     other_user = User.objects.create_user(
        username="otheruser",
        password="otherpass123",
    )

     self.client.login(
        username="otheruser",
        password="otherpass123",
    )

     response = self.client.get(
        reverse(
            "applications:detail",
            kwargs={"slug": self.application.slug},
        )
    )

     self.assertEqual(response.status_code, 404)
     
    def test_application_list_shows_only_users_applications(self):
     other_user = User.objects.create_user(
        username="otheruser",
        password="otherpass123",
    )

     Application.objects.create(
        user=other_user,
        company=self.company,
        position="Frontend Developer",
        status="applied",
        application_date=self.application.application_date,
        notes="Other user's application",
    )

     self.client.login(
        username="testuser",
        password="testpass123",
    )

     response = self.client.get(
        reverse("applications:list")
    )

     self.assertContains(
        response,
        "Django Backend Developer",
    )

     self.assertNotContains(
        response,
        "Frontend Developer",
    )
     
    def test_application_create_requires_login(self):
     response = self.client.get(
        reverse("applications:create")
    )

     self.assertEqual(response.status_code, 302)