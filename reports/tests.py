from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from applications.models import Application
from companies.models import Company
from notes.models import Note
from datetime import timedelta

from django.utils import timezone

from interviews.models import Interview


class ReportDashboardTest(TestCase):

    def setUp(self):
     self.user = User.objects.create_user(
        username="reportuser",
        password="Testpass123",
    )

     self.other_user = User.objects.create_user(
        username="otherreportuser",
        password="Testpass123",
    )

    def test_report_dashboard_view(self):
        self.client.login(
            username="reportuser",
            password="Testpass123",
        )

        response = self.client.get(
            reverse("reports:report_dashboard")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "reports/report_dashboard.html",
        )
        
    def test_report_dashboard_requires_login(self):
     report_url = reverse(
        "reports:report_dashboard"
    )

     login_url = reverse(
        "accounts:login"
    )

     response = self.client.get(
        report_url
    )

     self.assertRedirects(
        response,
        f"{login_url}?next={report_url}",
    )
     
    def test_report_dashboard_returns_zero_counts_for_empty_data(self):
     self.client.login(
        username="reportuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:report_dashboard")
    )

     expected_zero_values = [
        "total_applications",
        "accepted_applications",
        "rejected_applications",
        "interview_applications",
        "total_interviews",
        "scheduled_interviews",
        "completed_interviews",
        "total_notes",
        "high_priority_notes",
        "pinned_notes",
    ]

     for context_key in expected_zero_values:
         self.assertEqual(
            response.context[context_key],
            0,
        )
         
         
    def test_application_statistics_are_calculated_correctly(self):
     company = Company.objects.create(
        name="Test Şirketi",
        website="https://example.com",
        location="İstanbul",
    )

     application_data = [
        {
            "position": "Backend Developer",
            "status": "accepted",
        },
        {
            "position": "Python Developer",
            "status": "rejected",
        },
        {
            "position": "Django Developer",
            "status": "rejected",
        },
        {
            "position": "Junior Backend Developer",
            "status": "interview",
        },
        {
            "position": "Software Developer",
            "status": "applied",
        },
    ]

     for data in application_data:
        Application.objects.create(
            user=self.user,
            company=company,
            position=data["position"],
            status=data["status"],
            notes="Rapor testi için oluşturuldu.",
        )

     self.client.login(
        username="reportuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:report_dashboard")
    )

     self.assertEqual(
        response.context["total_applications"],
        5,
    )

     self.assertEqual(
        response.context["accepted_applications"],
        1,
    )

     self.assertEqual(
        response.context["rejected_applications"],
        2,
    )

     self.assertEqual(
        response.context["interview_applications"],
        1,
    )
     
    def test_interview_statistics_are_calculated_correctly(self):
     company = Company.objects.create(
        name="Görüşme Test Şirketi",
        website="https://interviewtest.com",
        location="Ankara",
    )

     application = Application.objects.create(
        user=self.user,
        company=company,
        position="Django Backend Developer",
        status="interview",
        notes="Görüşme istatistiği testi.",
    )

     interview_data = [
        {
            "interview_type": "technical",
            "status": "scheduled",
            "days": 1,
        },
        {
            "interview_type": "hr",
            "status": "scheduled",
            "days": 2,
        },
        {
            "interview_type": "manager",
            "status": "completed",
            "days": 3,
        },
        {
            "interview_type": "other",
            "status": "cancelled",
            "days": 4,
        },
    ]

     for data in interview_data:
        Interview.objects.create(
            application=application,
            interview_type=data["interview_type"],
            scheduled_at=(
                timezone.now()
                + timedelta(days=data["days"])
            ),
            status=data["status"],
            location="Online",
            interviewer_name="Test Görüşmeci",
            notes="Reports testi için oluşturuldu.",
        )

     self.client.login(
        username="reportuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:report_dashboard")
    )

     self.assertEqual(
        response.context["total_interviews"],
        4,
    )

     self.assertEqual(
        response.context["scheduled_interviews"],
        2,
    )

     self.assertEqual(
        response.context["completed_interviews"],
        1,
    )
     
    def test_note_statistics_are_calculated_correctly(self):
     note_data = [
        {
            "title": "Yüksek ve Sabit Not",
            "priority": "high",
            "is_pinned": True,
        },
        {
            "title": "Yüksek Öncelikli Not",
            "priority": "high",
            "is_pinned": False,
        },
        {
            "title": "Orta ve Sabit Not",
            "priority": "medium",
            "is_pinned": True,
        },
        {
            "title": "Düşük Öncelikli Not",
            "priority": "low",
            "is_pinned": False,
        },
    ]

     for data in note_data:
        Note.objects.create(
            user=self.user,
            title=data["title"],
            content="Reports testi için oluşturuldu.",
            category="general",
            priority=data["priority"],
            is_pinned=data["is_pinned"],
        )

     self.client.login(
        username="reportuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:report_dashboard")
    )

     self.assertEqual(
        response.context["total_notes"],
        4,
    )

     self.assertEqual(
        response.context["high_priority_notes"],
        2,
    )

     self.assertEqual(
        response.context["pinned_notes"],
        2,
    )
     
     
    def test_report_dashboard_uses_only_logged_in_users_data(self):
     company = Company.objects.create(
        name="İzolasyon Test Şirketi",
        website="https://isolationtest.com",
        location="İstanbul",
    )

     own_application = Application.objects.create(
        user=self.user,
        company=company,
        position="Django Developer",
        status="accepted",
        notes="Kendi başvurum.",
    )

     other_application = Application.objects.create(
        user=self.other_user,
        company=company,
        position="Python Developer",
        status="rejected",
        notes="Başka kullanıcının başvurusu.",
    )

     Interview.objects.create(
        application=own_application,
        interview_type="technical",
        scheduled_at=timezone.now() + timedelta(days=1),
        status="scheduled",
    )

     Interview.objects.create(
        application=other_application,
        interview_type="hr",
        scheduled_at=timezone.now() + timedelta(days=2),
        status="completed",
    )

     Note.objects.create(
        user=self.user,
        title="Kendi Notum",
        content="Bu not rapora dahil olmalı.",
        category="general",
        priority="high",
        is_pinned=True,
    )

     Note.objects.create(
        user=self.other_user,
        title="Başka Kullanıcının Notu",
        content="Bu not rapora dahil olmamalı.",
        category="general",
        priority="high",
        is_pinned=True,
    )

     self.client.login(
        username="reportuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:report_dashboard")
    )

     self.assertEqual(
        response.context["total_applications"],
        1,
    )

     self.assertEqual(
        response.context["accepted_applications"],
        1,
    )

     self.assertEqual(
        response.context["rejected_applications"],
        0,
    )

     self.assertEqual(
        response.context["total_interviews"],
        1,
    )

     self.assertEqual(
        response.context["scheduled_interviews"],
        1,
    )

     self.assertEqual(
        response.context["completed_interviews"],
        0,
    )

     self.assertEqual(
        response.context["total_notes"],
        1,
    )

     self.assertEqual(
        response.context["high_priority_notes"],
        1,
    )

     self.assertEqual(
        response.context["pinned_notes"],
        1,
    )
     
    def test_report_dashboard_uses_only_logged_in_users_data(self):
     company = Company.objects.create(
        name="İzolasyon Test Şirketi",
        website="https://isolationtest.com",
        location="İstanbul",
    )

     own_application = Application.objects.create(
        user=self.user,
        company=company,
        position="Django Developer",
        status="accepted",
        notes="Kendi başvurum.",
    )

     other_application = Application.objects.create(
        user=self.other_user,
        company=company,
        position="Python Developer",
        status="rejected",
        notes="Başka kullanıcının başvurusu.",
    )

     Interview.objects.create(
        application=own_application,
        interview_type="technical",
        scheduled_at=timezone.now() + timedelta(days=1),
        status="scheduled",
    )

     Interview.objects.create(
        application=other_application,
        interview_type="hr",
        scheduled_at=timezone.now() + timedelta(days=2),
        status="completed",
    )

     Note.objects.create(
        user=self.user,
        title="Kendi Notum",
        content="Bu not rapora dahil olmalı.",
        category="general",
        priority="high",
        is_pinned=True,
    )

     Note.objects.create(
        user=self.other_user,
        title="Başka Kullanıcının Notu",
        content="Bu not rapora dahil olmamalı.",
        category="general",
        priority="high",
        is_pinned=True,
    )

     self.client.login(
        username="reportuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:report_dashboard")
    )

     self.assertEqual(
        response.context["total_applications"],
        1,
    )

     self.assertEqual(
        response.context["accepted_applications"],
        1,
    )

     self.assertEqual(
        response.context["rejected_applications"],
        0,
    )

     self.assertEqual(
        response.context["total_interviews"],
        1,
    )

     self.assertEqual(
        response.context["scheduled_interviews"],
        1,
    )

     self.assertEqual(
        response.context["completed_interviews"],
        0,
    )

     self.assertEqual(
        response.context["total_notes"],
        1,
    )

     self.assertEqual(
        response.context["high_priority_notes"],
        1,
    )

     self.assertEqual(
        response.context["pinned_notes"],
        1,
    )