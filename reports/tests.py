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

        response = self.client.get(reverse("reports:report_dashboard"))

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "reports/report_dashboard.html",
        )

    def test_report_dashboard_requires_login(self):
        report_url = reverse("reports:report_dashboard")

        login_url = reverse("accounts:login")

        response = self.client.get(report_url)

        self.assertRedirects(
            response,
            f"{login_url}?next={report_url}",
        )

    def test_report_dashboard_returns_zero_counts_for_empty_data(self):
        self.client.login(
            username="reportuser",
            password="Testpass123",
        )

        response = self.client.get(reverse("reports:report_dashboard"))

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
            "acceptance_rate",
            "interview_rate",
            "interview_completion_rate",
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

        response = self.client.get(reverse("reports:report_dashboard"))

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
        
        self.assertEqual(
          response.context["acceptance_rate"],
          20.0,
        )
        
        self.assertEqual(
          response.context["interview_rate"],
          20.0,
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
                scheduled_at=(timezone.now() + timedelta(days=data["days"])),
                status=data["status"],
                location="Online",
                interviewer_name="Test Görüşmeci",
                notes="Reports testi için oluşturuldu.",
            )

        self.client.login(
            username="reportuser",
            password="Testpass123",
        )

        response = self.client.get(reverse("reports:report_dashboard"))

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
        
        
        self.assertEqual(
         response.context["interview_completion_rate"],
         25.0,
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

        response = self.client.get(reverse("reports:report_dashboard"))

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

        response = self.client.get(reverse("reports:report_dashboard"))

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

        response = self.client.get(reverse("reports:report_dashboard"))

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


    def test_recent_applications_are_calculated_correctly(self):
     company = Company.objects.create(
        name="Recent Test Şirketi",
        website="https://recenttest.com",
        location="İstanbul",
    )

     Application.objects.create(
        user=self.user,
        company=company,
        position="Recent Django Developer",
        status="applied",
        application_date=timezone.now().date(),
        notes="Son 30 gün testi.",
    )

     self.client.login(
        username="reportuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:report_dashboard")
    )

     self.assertEqual(
        response.context["recent_applications"],
        1,
    )
     
     
    def test_old_applications_are_not_counted_as_recent(self):
     company = Company.objects.create(
        name="Eski Başvuru Test Şirketi",
        website="https://oldapplicationtest.com",
        location="İstanbul",
    )

     old_application = Application.objects.create(
        user=self.user,
        company=company,
        position="Eski Django Developer",
        status="applied",
        notes="30 günden eski başvuru.",
    )

     Application.objects.filter(
        pk=old_application.pk,
    ).update(
        application_date=timezone.now().date() - timedelta(days=31),
    )

     self.client.login(
        username="reportuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:report_dashboard")
    )

     self.assertEqual(
        response.context["recent_applications"],
        0,
    )
     
    def test_top_company_is_calculated_correctly(self):
     company_one = Company.objects.create(
        name="Birinci Şirket",
        website="https://birincisirket.com",
        location="İstanbul",
    )

     company_two = Company.objects.create(
        name="İkinci Şirket",
        website="https://ikincisirket.com",
        location="Ankara",
    )

     Application.objects.create(
        user=self.user,
        company=company_one,
        position="Backend Developer",
        status="applied",
        notes="Test başvurusu 1",
    )

     Application.objects.create(
        user=self.user,
        company=company_one,
        position="Django Developer",
        status="applied",
        notes="Test başvurusu 2",
    )

     Application.objects.create(
        user=self.user,
        company=company_two,
        position="Python Developer",
        status="applied",
        notes="Test başvurusu 3",
    )

     self.client.login(
        username="reportuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:report_dashboard")
    )

     self.assertEqual(
        response.context["top_company"]["company__name"],
        "Birinci Şirket",
    )

     self.assertEqual(
        response.context["top_company"]["total"],
        2,
    )
     
          
    def test_top_company_respects_user_isolation(self):
     other_user = User.objects.create_user(
        username="otheruser",
        password="Testpass123",
    )

     my_company = Company.objects.create(
        name="Benim Şirketim",
        website="https://mycompany.com",
        location="İstanbul",
    )

     other_company = Company.objects.create(
        name="Başka Kullanıcının Şirketi",
        website="https://othercompany.com",
        location="Ankara",
    )

     Application.objects.create(
        user=self.user,
        company=my_company,
        position="Django Developer",
        status="applied",
        notes="Benim başvurum.",
    )

     for _ in range(5):
        Application.objects.create(
            user=other_user,
            company=other_company,
            position="Backend Developer",
            status="applied",
            notes="Başka kullanıcının başvurusu.",
        )

     self.client.login(
        username="reportuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:report_dashboard")
    )

     self.assertEqual(
        response.context["top_company"]["company__name"],
        "Benim Şirketim",
    )

     self.assertEqual(
        response.context["top_company"]["total"],
        1,
    )
     
     
    def test_advanced_report_metrics_respect_user_isolation(self):
     company = Company.objects.create(
        name="Gelişmiş Rapor İzolasyon Şirketi",
        website="https://advancedreporttest.com",
        location="İstanbul",
    )

     Application.objects.create(
        user=self.user,
        company=company,
        position="Django Developer",
        status="accepted",
        notes="Kendi başvurum.",
    )

     for _ in range(4):
        Application.objects.create(
            user=self.other_user,
            company=company,
            position="Python Developer",
            status="rejected",
            notes="Başka kullanıcının başvurusu.",
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
        response.context["acceptance_rate"],
        100.0,
    )

     self.assertEqual(
        response.context["rejection_rate"],
        0.0,
    )

     self.assertEqual(
        response.context["recent_applications"],
        1,
    )
     

class ApplicationCSVExportTest(TestCase):

    def test_csv_export_requires_login(self):
        response = self.client.get(
            reverse("reports:export_applications_csv")
        )

        self.assertEqual(
            response.status_code,
            302,
        )
        
    def test_logged_in_user_can_export_csv(self):
     user = User.objects.create_user(
        username="csvuser",
        password="Testpass123",
    )

     self.client.login(
        username="csvuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:export_applications_csv")
    )

     self.assertEqual(
        response.status_code,
        200,
    )

     self.assertEqual(
        response["Content-Type"],
        "text/csv; charset=utf-8",
    )
     
     
    def test_csv_export_has_correct_filename(self):
     user = User.objects.create_user(
        username="csvfilenameuser",
        password="Testpass123",
    )

     self.client.login(
        username="csvfilenameuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:export_applications_csv")
    )

     self.assertEqual(
        response["Content-Disposition"],
        'attachment; filename="applications.csv"',
    )
     
     
    def test_csv_export_contains_only_logged_in_user_data(self):
     user1 = User.objects.create_user(
        username="csvuser1",
        password="Testpass123",
    )

     user2 = User.objects.create_user(
        username="csvuser2",
        password="Testpass123",
    )

     company = Company.objects.create(
        name="CSV Test Company",
        website="https://csvtest.com",
        location="İstanbul",
    )

     Application.objects.create(
        user=user1,
        company=company,
        position="Django Backend Developer",
        status="applied",
        notes="User 1 application",
    )

     Application.objects.create(
        user=user2,
        company=company,
        position="Python Developer",
        status="applied",
        notes="User 2 application",
    )

     self.client.login(
        username="csvuser1",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:export_applications_csv")
    )

     content = response.content.decode("utf-8-sig")

     self.assertIn(
        "Django Backend Developer",
        content,
    )

     self.assertNotIn(
        "Python Developer",
        content,
    )
     
     
    def test_csv_export_contains_correct_headers_and_data(self):
     user = User.objects.create_user(
        username="csvcontentuser",
        password="Testpass123",
    )

     company = Company.objects.create(
        name="CSV İçerik Şirketi",
        website="https://csvcontent.com",
        location="İstanbul",
    )

     Application.objects.create(
        user=user,
        company=company,
        position="Django Developer",
        status="accepted",
        notes="CSV içerik testi",
    )

     self.client.login(
        username="csvcontentuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:export_applications_csv")
    )

     content = response.content.decode("utf-8-sig")

     self.assertIn(
        "Company;Position;Status;Application Date",
        content,
    )

     self.assertIn(
        "CSV İçerik Şirketi;Django Developer;Kabul Edildi",
        content,
    )
     
    def test_csv_export_works_with_no_applications(self):
     user = User.objects.create_user(
        username="csvemptyuser",
        password="Testpass123",
    )

     self.client.login(
        username="csvemptyuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reports:export_applications_csv")
    )

     content = response.content.decode("utf-8-sig")

     self.assertEqual(
        response.status_code,
        200,
    )

     self.assertIn(
        "Company;Position;Status;Application Date",
        content,
    )