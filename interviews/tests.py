from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from applications.models import Application
from companies.models import Company
from .forms import InterviewForm
from .models import Interview
from django.urls import reverse


class InterviewModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="Testpass123",
        )

        self.company = Company.objects.create(
            name="Test Şirketi",
            website="https://example.com",
            location="İstanbul",
        )

        self.application = Application.objects.create(
            user=self.user,
            company=self.company,
            position="Django Backend Developer",
            status="applied",
            notes="Test başvurusu",
        )

        self.interview = Interview.objects.create(
            application=self.application,
            interview_type="technical",
            scheduled_at=timezone.now(),
            status="scheduled",
            location="İstanbul",
            interviewer_name="Test Görüşmeci",
            notes="Teknik görüşme testi",
        )

    def test_interview_string_representation(self):
        expected_value = "Test Şirketi - Teknik Görüşme"

        self.assertEqual(
            str(self.interview),
            expected_value,
        )
        
    def test_default_status_is_scheduled(self):
     interview = Interview.objects.create(
        application=self.application,
        interview_type="technical",
        scheduled_at=timezone.now(),
    )

     self.assertEqual(
        interview.status,
        "scheduled",
    )
     
    def test_default_ordering(self):
     self.assertEqual(
        Interview._meta.ordering,
        ["scheduled_at"],
    )
     
    def test_interview_belongs_to_application(self):
     self.assertEqual(
        self.interview.application,
        self.application,
    )
     
    
    def test_application_related_name(self):
     self.assertEqual(
        self.application.interviews.count(),
        1,
    )

     self.assertEqual(
        self.application.interviews.first(),
        self.interview,
    )
     
    def test_created_at_is_set_automatically(self):
     self.assertIsNotNone(
        self.interview.created_at,
    )
     
    def test_interview_count(self):
     self.assertEqual(
        Interview.objects.count(),
        1,
    )
     

class InterviewFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="formuser",
            password="Testpass123",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="Testpass123",
        )

        self.company = Company.objects.create(
            name="Form Test Şirketi",
            website="https://formtest.com",
            location="İstanbul",
        )

        self.user_application = Application.objects.create(
            user=self.user,
            company=self.company,
            position="Backend Developer",
            status="applied",
            notes="Kullanıcının başvurusu",
        )

        self.other_application = Application.objects.create(
            user=self.other_user,
            company=self.company,
            position="Frontend Developer",
            status="applied",
            notes="Diğer kullanıcının başvurusu",
        )

    def test_form_contains_expected_fields(self):
        form = InterviewForm()

        expected_fields = [
            "application",
            "interview_type",
            "scheduled_at",
            "status",
            "location",
            "meeting_link",
            "interviewer_name",
            "notes",
        ]

        self.assertEqual(
            list(form.fields.keys()),
            expected_fields,
        )

    def test_application_queryset_contains_only_user_applications(self):
        form = InterviewForm(
            user=self.user,
        )

        application_queryset = form.fields["application"].queryset

        self.assertIn(
            self.user_application,
            application_queryset,
        )

        self.assertNotIn(
            self.other_application,
            application_queryset,
        )

        self.assertEqual(
            application_queryset.count(),
            1,
        )

    def test_form_contains_expected_fields(self):
        form = InterviewForm()

        expected_fields = [
            "application",
            "interview_type",
            "scheduled_at",
            "status",
            "location",
            "meeting_link",
            "interviewer_name",
            "notes",
        ]

        self.assertEqual(
            list(form.fields.keys()),
            expected_fields,
        )
        
        
    def test_form_is_valid_with_correct_data(self):
     scheduled_at = (
        timezone.now() + timedelta(days=1)
    ).strftime("%Y-%m-%dT%H:%M")

     form = InterviewForm(
        data={
            "application": self.user_application.id,
            "interview_type": "technical",
            "scheduled_at": scheduled_at,
            "status": "scheduled",
            "location": "İstanbul",
            "meeting_link": "https://meet.example.com/interview",
            "interviewer_name": "Ayşe Yılmaz",
            "notes": "Django ve REST API konularına hazırlan.",
        },
         user=self.user,
    )

     self.assertTrue(
        form.is_valid(),
        form.errors,
    )
     
    def test_form_is_invalid_when_required_fields_are_missing(self):
     form = InterviewForm(
        data={
            "application": "",
            "interview_type": "",
            "scheduled_at": "",
            "status": "scheduled",
            "location": "",
            "meeting_link": "",
            "interviewer_name": "",
            "notes": "",
        },
        user=self.user,
    )

     self.assertFalse(
        form.is_valid(),
    )

     self.assertIn(
        "application",
        form.errors,
    )

     self.assertIn(
        "interview_type",
        form.errors,
    )

     self.assertIn(
        "scheduled_at",
        form.errors,
    )
     
class InterviewViewTest(TestCase):

    def setUp(self):
     self.user = User.objects.create_user(
        username="viewuser",
        password="Testpass123",
    )

     self.other_user = User.objects.create_user(
        username="otherviewuser",
        password="Testpass123",
    )

     self.company = Company.objects.create(
        name="View Test Şirketi",
        website="https://viewtest.com",
        location="İstanbul",
    )

     self.user_application = Application.objects.create(
        user=self.user,
        company=self.company,
        position="Django Backend Developer",
        status="applied",
        notes="Kullanıcı başvurusu",
    )

     self.other_application = Application.objects.create(
        user=self.other_user,
        company=self.company,
        position="Frontend Developer",
        status="applied",
        notes="Diğer kullanıcı başvurusu",
    )

     self.user_interview = Interview.objects.create(
        application=self.user_application,
        interview_type="technical",
        scheduled_at=timezone.now() + timedelta(days=1),
        status="scheduled",
        location="İstanbul",
    )

     self.other_interview = Interview.objects.create(
        application=self.other_application,
        interview_type="hr",
        scheduled_at=timezone.now() + timedelta(days=2),
        status="scheduled",
        location="Ankara",
    )

    def test_interview_list_requires_login(self):
        response = self.client.get(
            reverse("interviews:interview_list")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_interview_list_redirects_to_login(self):
        interview_list_url = reverse(
            "interviews:interview_list"
        )

        login_url = reverse(
            "accounts:login"
        )

        response = self.client.get(
            interview_list_url
        )

        self.assertRedirects(
            response,
            f"{login_url}?next={interview_list_url}",
        )

    def test_logged_in_user_can_access_interview_list(self):
        self.client.login(
            username="viewuser",
            password="Testpass123",
        )

        response = self.client.get(
            reverse("interviews:interview_list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "interviews/interview_list.html",
        )

    def test_interview_list_requires_login(self):
        response = self.client.get(
            reverse("interviews:interview_list")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_interview_list_redirects_to_login(self):
        interview_list_url = reverse(
            "interviews:interview_list"
        )

        login_url = reverse(
            "accounts:login"
        )

        response = self.client.get(
            interview_list_url
        )

        self.assertRedirects(
            response,
            f"{login_url}?next={interview_list_url}",
        )
        
    def test_interview_list_contains_only_logged_in_user_interviews(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("interviews:interview_list")
    )

     interviews = response.context["interviews"]

     self.assertIn(
        self.user_interview,
        interviews,
    )

     self.assertNotIn(
        self.other_interview,
        interviews,
    )

     self.assertEqual(
        interviews.count(),
        1,
    )
     
     
    def test_user_can_access_own_interview_detail(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse(
            "interviews:interview_detail",
            kwargs={
                "pk": self.user_interview.pk,
            },
        )
    )

     self.assertEqual(
        response.status_code,
        200,
    )

     self.assertTemplateUsed(
        response,
        "interviews/interview_detail.html",
    )

     self.assertEqual(
        response.context["interview"],
        self.user_interview,
    )
     
     
    def test_user_cannot_access_other_users_interview(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse(
            "interviews:interview_detail",
            kwargs={
                "pk": self.other_interview.pk,
            },
        )
    )

     self.assertEqual(
        response.status_code,
        404,
    )
     
    def test_create_view_get_request(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse(
            "interviews:interview_create",
        )
    )

     self.assertEqual(
        response.status_code,
        200,
    )

     self.assertTemplateUsed(
        response,
        "interviews/interview_form.html",
    )

     self.assertIn(
        "form",
        response.context,
    )
     
    def test_create_view_post_request(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse("interviews:interview_create"),
        {
            "application": self.user_application.id,
            "interview_type": "technical",
            "scheduled_at": (
                timezone.now() + timedelta(days=5)
            ).strftime("%Y-%m-%dT%H:%M"),
            "status": "scheduled",
            "location": "İstanbul",
            "meeting_link": "",
            "interviewer_name": "Ahmet Yılmaz",
            "notes": "POST testi",
        },
    )

     self.assertEqual(
        response.status_code,
        302,
    )

     self.assertEqual(
        Interview.objects.filter(
            application=self.user_application
        ).count(),
        2,
    )
     
    def test_update_view_get_request(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse(
            "interviews:interview_update",
            kwargs={
                "pk": self.user_interview.pk,
            },
        )
    )

     self.assertEqual(
        response.status_code,
        200,
    )

     self.assertTemplateUsed(
        response,
        "interviews/interview_form.html",
    )

     self.assertIn(
        "form",
        response.context,
    )

     self.assertEqual(
        response.context["interview"],
        self.user_interview,
    )
     
    def test_update_view_post_request(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse(
            "interviews:interview_update",
            kwargs={
                "pk": self.user_interview.pk,
            },
        ),
        {
            "application": self.user_application.id,
            "interview_type": "manager",
            "scheduled_at": (
                timezone.now() + timedelta(days=10)
            ).strftime("%Y-%m-%dT%H:%M"),
            "status": "completed",
            "location": "Ankara",
            "meeting_link": "",
            "interviewer_name": "Mehmet Kaya",
            "notes": "Güncellendi",
        },
    )

     self.assertEqual(
        response.status_code,
        302,
    )

     self.user_interview.refresh_from_db()

     self.assertEqual(
        self.user_interview.interview_type,
        "manager",
    )

     self.assertEqual(
        self.user_interview.status,
        "completed",
    )

     self.assertEqual(
        self.user_interview.location,
        "Ankara",
    )

     self.assertEqual(
        self.user_interview.interviewer_name,
        "Mehmet Kaya",
    )

     self.assertEqual(
        self.user_interview.notes,
        "Güncellendi",
    )
     
    def test_delete_view_get_request(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse(
            "interviews:interview_delete",
            kwargs={
                "pk": self.user_interview.pk,
            },
        )
    )

     self.assertEqual(
        response.status_code,
        200,
    )

     self.assertTemplateUsed(
        response,
        "interviews/interview_confirm_delete.html",
    )

     self.assertEqual(
        response.context["interview"],
        self.user_interview,
    )
    
    def test_delete_view_post_request(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     interview_id = self.user_interview.id

     response = self.client.post(
        reverse(
            "interviews:interview_delete",
            kwargs={
                "pk": self.user_interview.pk,
            },
        )
    )

     self.assertEqual(
        response.status_code,
        302,
    )

     self.assertFalse(
        Interview.objects.filter(
            id=interview_id,
        ).exists()
    )
     
    def test_user_cannot_delete_other_users_interview(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse(
            "interviews:interview_delete",
            kwargs={
                "pk": self.other_interview.pk,
            },
        )
    )

     self.assertEqual(
        response.status_code,
        404,
    )

     self.assertTrue(
        Interview.objects.filter(
            pk=self.other_interview.pk,
        ).exists()
    )
     
    def test_user_cannot_update_other_users_interview(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     original_status = self.other_interview.status
     original_notes = self.other_interview.notes

     response = self.client.post(
        reverse(
            "interviews:interview_update",
            kwargs={
                "pk": self.other_interview.pk,
            },
        ),
        {
            "application": self.other_application.id,
            "interview_type": "final",
            "scheduled_at": (
                timezone.now() + timedelta(days=15)
            ).strftime("%Y-%m-%dT%H:%M"),
            "status": "completed",
            "location": "İzmir",
            "meeting_link": "",
            "interviewer_name": "Yetkisiz Güncelleme",
            "notes": "Bu veri değiştirilmemeli",
        },
    )

     self.assertEqual(
        response.status_code,
        404,
    )

     self.other_interview.refresh_from_db()

     self.assertEqual(
        self.other_interview.status,
        original_status,
    )

     self.assertEqual(
        self.other_interview.notes,
        original_notes,
    )
    
    def test_user_cannot_create_interview_for_other_users_application(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     interview_count_before = Interview.objects.count()

     response = self.client.post(
        reverse("interviews:interview_create"),
        {
            "application": self.other_application.id,
            "interview_type": "technical",
            "scheduled_at": (
                timezone.now() + timedelta(days=5)
            ).strftime("%Y-%m-%dT%H:%M"),
            "status": "scheduled",
            "location": "İstanbul",
            "meeting_link": "",
            "interviewer_name": "Yetkisiz Görüşmeci",
            "notes": "Bu kayıt oluşturulmamalı",
        },
    )

     self.assertEqual(
        response.status_code,
        200,
    )

     self.assertEqual(
        Interview.objects.count(),
        interview_count_before,
    )

     self.assertIn(
        "application",
        response.context["form"].errors,
    )
     
    def test_interview_create_requires_login(self):
     create_url = reverse(
        "interviews:interview_create"
    )

     login_url = reverse(
        "accounts:login"
    )

     response = self.client.get(
        create_url
    )

     self.assertRedirects(
        response,
        f"{login_url}?next={create_url}",
    )
     
    def test_interview_update_requires_login(self):
     update_url = reverse(
        "interviews:interview_update",
        kwargs={
            "pk": self.user_interview.pk,
        },
    )

     login_url = reverse(
        "accounts:login"
    )

     response = self.client.get(
        update_url
    )

     self.assertRedirects(
        response,
        f"{login_url}?next={update_url}",
    )
     
    def test_interview_delete_requires_login(self):
     delete_url = reverse(
        "interviews:interview_delete",
        kwargs={
            "pk": self.user_interview.pk,
        },
    )

     login_url = reverse(
        "accounts:login"
    )

     response = self.client.get(
        delete_url
    )

     self.assertRedirects(
        response,
        f"{login_url}?next={delete_url}",
    )
     
    def test_interview_detail_requires_login(self):
     detail_url = reverse(
        "interviews:interview_detail",
        kwargs={
            "pk": self.user_interview.pk,
        },
    )

     login_url = reverse(
        "accounts:login"
    )

     response = self.client.get(
        detail_url
    )

     self.assertRedirects(
        response,
        f"{login_url}?next={detail_url}",
    )
     
    def test_create_view_redirects_to_interview_list(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse("interviews:interview_create"),
        {
            "application": self.user_application.id,
            "interview_type": "technical",
            "scheduled_at": (
                timezone.now() + timedelta(days=3)
            ).strftime("%Y-%m-%dT%H:%M"),
            "status": "scheduled",
            "location": "İstanbul",
            "meeting_link": "",
            "interviewer_name": "Ali Veli",
            "notes": "Redirect testi",
        },
    )

     self.assertRedirects(
        response,
        reverse("interviews:interview_list"),
    )
     
    def test_update_view_redirects_to_detail(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse(
            "interviews:interview_update",
            kwargs={
                "pk": self.user_interview.pk,
            },
        ),
        {
            "application": self.user_application.id,
            "interview_type": "manager",
            "scheduled_at": (
                timezone.now() + timedelta(days=7)
            ).strftime("%Y-%m-%dT%H:%M"),
            "status": "completed",
            "location": "Ankara",
            "meeting_link": "",
            "interviewer_name": "Ayşe Demir",
            "notes": "Redirect testi",
        },
    )

     self.assertRedirects(
        response,
        reverse(
            "interviews:interview_detail",
            kwargs={
                "pk": self.user_interview.pk,
            },
        ),
    )