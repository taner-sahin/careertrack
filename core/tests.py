from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from applications.models import Application
from companies.models import Company


class HomeViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
        )

        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123',
        )

        self.company = Company.objects.create(
            user=self.user,
            name='Test Company',
            website='https://testcompany.com',
            location='İstanbul, Türkiye',
        )

        self.other_company = Company.objects.create(
            user=self.other_user,
            name='Other Company',
            website='https://othercompany.com',
            location='Ankara, Türkiye',
        )

        self.application = Application.objects.create(
            user=self.user,
            company=self.company,
            position='Django Backend Developer',
            status='applied',
        )

        self.other_application = Application.objects.create(
            user=self.other_user,
            company=self.other_company,
            position='Python Developer',
            status='accepted',
        )

        self.url = reverse('core:home')

    def test_home_requires_login(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_home_opens_for_logged_in_user(self):
        self.client.login(
            username='testuser',
            password='testpass123',
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            'home.html',
        )

    def test_dashboard_shows_only_logged_in_users_applications(self):
        self.client.login(
            username='testuser',
            password='testpass123',
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.context['total_applications'],
            1,
        )

    def test_dashboard_counts_only_logged_in_users_companies(self):
        self.client.login(
            username='testuser',
            password='testpass123',
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.context['total_companies'],
            1,
        )

    def test_dashboard_recent_applications_belong_to_logged_in_user(self):
        self.client.login(
            username='testuser',
            password='testpass123',
        )

        response = self.client.get(self.url)

        recent_applications = response.context[
            'recent_applications'
        ]

        self.assertIn(
            self.application,
            recent_applications,
        )

        self.assertNotIn(
            self.other_application,
            recent_applications,
        )

    def test_dashboard_recent_companies_are_user_isolated(self):
        self.client.login(
            username='testuser',
            password='testpass123',
        )

        response = self.client.get(self.url)

        recent_companies = response.context[
            'recent_companies'
        ]

        self.assertIn(
            self.company,
            recent_companies,
        )

        self.assertNotIn(
            self.other_company,
            recent_companies,
        )