from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from .forms import ReminderForm
from .models import Reminder
from applications.models import Application
from companies.models import Company
from interviews.models import Interview
from django.urls import reverse

class ReminderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="reminderuser",
            password="Testpass123",
        )

        self.reminder = Reminder.objects.create(
            user=self.user,
            title="Papara görüşmesine hazırlan",
            reminder_type="interview",
            remind_at=timezone.now(),
        )

    def test_reminder_string_representation(self):
        self.assertEqual(
            str(self.reminder),
            "Papara görüşmesine hazırlan",
        )
    def test_reminder_is_not_completed_by_default(self):
     self.assertFalse(self.reminder.is_completed)
     
     
    def test_reminder_type_default_is_other(self):
     reminder = Reminder.objects.create(
        user=self.user,
        title="CV güncelle",
        remind_at=timezone.now(),
    )

     self.assertEqual(
        reminder.reminder_type,
        "other",
    )
     
    def test_application_and_interview_can_be_empty(self):
     reminder = Reminder.objects.create(
        user=self.user,
        title="CV güncelle",
        remind_at=timezone.now(),
    )

     self.assertIsNone(
        reminder.application
    )

     self.assertIsNone(
        reminder.interview
    )
     
    def test_reminder_type_choices_are_correct(self):
     field = Reminder._meta.get_field(
        "reminder_type"
    )

     self.assertEqual(
        field.choices,
        [
            ("application", "Başvuru"),
            ("interview", "Görüşme"),
            ("cv", "CV"),
            ("other", "Diğer"),
        ],
    )
     
     
class ReminderFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="formuser",
            password="Testpass123",
        )

    def test_reminder_form_is_valid_with_required_fields(self):
        form = ReminderForm(
            data={
                "title": "CV güncelle",
                "reminder_type": "cv",
                "remind_at": "2026-08-20T10:00",
                "notes": "",
                "is_completed": False,
            },
            user=self.user,
        )

        self.assertTrue(
            form.is_valid()
        )
        
    def test_application_queryset_contains_only_current_user_applications(self):
     other_user = User.objects.create_user(
        username="otheruser",
        password="Otherpass123",
    )

     company = Company.objects.create(
        name="Test Company",
    )

     own_application = Application.objects.create(
        user=self.user,
        company=company,
        position="Django Developer",
    )

     other_application = Application.objects.create(
        user=other_user,
        company=company,
        position="Python Developer",
    )

     form = ReminderForm(
        user=self.user,
    )

     application_queryset = form.fields[
        "application"
    ].queryset

     self.assertIn(
        own_application,
        application_queryset,
    )

     self.assertNotIn(
        other_application,
        application_queryset,
    )
     
     
    def test_interview_queryset_contains_only_current_user_interviews(self):
     other_user = User.objects.create_user(
        username="otherinterviewuser",
        password="Otherpass123",
    )

     company = Company.objects.create(
        name="Interview Test Company",
    )

     own_application = Application.objects.create(
        user=self.user,
        company=company,
        position="Django Developer",
    )

     other_application = Application.objects.create(
        user=other_user,
        company=company,
        position="Python Developer",
    )

     own_interview = Interview.objects.create(
        application=own_application,
        interview_type="technical",
        scheduled_at=timezone.now(),
    )

     other_interview = Interview.objects.create(
        application=other_application,
        interview_type="hr",
        scheduled_at=timezone.now(),
    )

     form = ReminderForm(
        user=self.user,
    )

     interview_queryset = form.fields[
        "interview"
    ].queryset

     self.assertIn(
        own_interview,
        interview_queryset,
    )

     self.assertNotIn(
        other_interview,
        interview_queryset,
    )
     
     
class ReminderViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="viewuser",
            password="Testpass123",
        )

        self.reminder = Reminder.objects.create(
            user=self.user,
            title="Görüşmeye hazırlan",
            reminder_type="interview",
            remind_at=timezone.now(),
        )

    def test_reminder_list_page_opens_for_logged_in_user(self):
        self.client.login(
            username="viewuser",
            password="Testpass123",
        )

        response = self.client.get(
            reverse("reminders:reminder_list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "reminders/reminder_list.html",
        )
        
    def test_reminder_list_requires_login(self):
     reminder_list_url = reverse(
        "reminders:reminder_list"
    )

     login_url = reverse(
        "accounts:login"
    )

     response = self.client.get(
        reminder_list_url
    )

     self.assertRedirects(
        response,
        f"{login_url}?next={reminder_list_url}",
    )
     
     
    def test_reminder_list_shows_only_current_user_reminders(self):
     other_user = User.objects.create_user(
        username="otherlistuser",
        password="Otherpass123",
    )

     other_reminder = Reminder.objects.create(
        user=other_user,
        title="Başka kullanıcının hatırlatıcısı",
        reminder_type="other",
        remind_at=timezone.now(),
    )

     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("reminders:reminder_list")
    )

     reminders = response.context["reminders"]

     self.assertIn(
        self.reminder,
        reminders,
    )

     self.assertNotIn(
        other_reminder,
        reminders,
    )
     
    
    def test_reminder_detail_page_opens_for_owner(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse(
            "reminders:reminder_detail",
            kwargs={
                "pk": self.reminder.pk,
            },
        )
    )

     self.assertEqual(
        response.status_code,
        200,
    )

     self.assertTemplateUsed(
        response,
        "reminders/reminder_detail.html",
    )

     self.assertEqual(
        response.context["reminder"],
        self.reminder,
    )
     
    
    def test_user_cannot_access_other_users_reminder_detail(self):
     other_user = User.objects.create_user(
        username="otherdetailuser",
        password="Otherpass123",
    )

     other_reminder = Reminder.objects.create(
        user=other_user,
        title="Başka kullanıcının reminder kaydı",
        reminder_type="other",
        remind_at=timezone.now(),
    )

     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse(
            "reminders:reminder_detail",
            kwargs={
                "pk": other_reminder.pk,
            },
        )
    )

     self.assertEqual(
        response.status_code,
        404,
    )
     
     
     
    def test_user_can_create_reminder(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse("reminders:reminder_create"),
        {
            "title": "Yeni Reminder",
            "reminder_type": "cv",
            "remind_at": "2026-08-20T10:00",
            "notes": "CV güncellenecek.",
            "is_completed": False,
        },
    )

     self.assertEqual(
        response.status_code,
        302,
    )

     created_reminder = Reminder.objects.get(
        title="Yeni Reminder"
    )

     self.assertEqual(
        created_reminder.user,
        self.user,
    )

     self.assertEqual(
        created_reminder.reminder_type,
        "cv",
    )

     self.assertFalse(
        created_reminder.is_completed,
    )
     
     
    def test_user_can_update_reminder(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse(
            "reminders:reminder_update",
            kwargs={
                "pk": self.reminder.pk,
            },
        ),
        {
            "title": "Güncellenmiş Hatırlatıcı",
            "reminder_type": "cv",
            "remind_at": "2026-08-25T12:00",
            "notes": "Güncellenmiş not.",
            "is_completed": True,
        },
    )

     self.assertEqual(
        response.status_code,
        302,
    )

     self.reminder.refresh_from_db()

     self.assertEqual(
        self.reminder.title,
        "Güncellenmiş Hatırlatıcı",
    )

     self.assertEqual(
        self.reminder.reminder_type,
        "cv",
    )

     self.assertEqual(
        self.reminder.notes,
        "Güncellenmiş not.",
    )

     self.assertTrue(
        self.reminder.is_completed,
    )

     self.assertEqual(
        Reminder.objects.count(),
        1,
    )
     
    def test_user_can_delete_reminder(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse(
            "reminders:reminder_delete",
            kwargs={
                "pk": self.reminder.pk,
            },
        )
    )

     self.assertEqual(
        response.status_code,
        302,
    )

     self.assertFalse(
        Reminder.objects.filter(
            pk=self.reminder.pk
        ).exists()
    )
     
    def test_user_cannot_update_other_users_reminder(self):
     other_user = User.objects.create_user(
        username="otherupdateuser",
        password="Otherpass123",
    )

     other_reminder = Reminder.objects.create(
        user=other_user,
        title="Başkasının hatırlatıcısı",
        reminder_type="other",
        remind_at=timezone.now(),
    )

     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse(
            "reminders:reminder_update",
            kwargs={
                "pk": other_reminder.pk,
            },
        ),
        {
            "title": "İzinsiz güncelleme",
            "reminder_type": "cv",
            "remind_at": "2026-08-30T10:00",
        },
    )

     self.assertEqual(
        response.status_code,
        404,
    )

     other_reminder.refresh_from_db()

     self.assertEqual(
        other_reminder.title,
        "Başkasının hatırlatıcısı",
    )
     
    def test_user_cannot_delete_other_users_reminder(self):
     other_user = User.objects.create_user(
        username="otherdeleteuser",
        password="Otherpass123",
    )

     other_reminder = Reminder.objects.create(
        user=other_user,
        title="Başkasının silinemez hatırlatıcısı",
        reminder_type="other",
        remind_at=timezone.now(),
    )

     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse(
            "reminders:reminder_delete",
            kwargs={
                "pk": other_reminder.pk,
            },
        )
    )

     self.assertEqual(
        response.status_code,
        404,
    )

     self.assertTrue(
        Reminder.objects.filter(
            pk=other_reminder.pk
        ).exists()
    )
     
    def test_reminder_create_requires_login(self):
     create_url = reverse(
        "reminders:reminder_create"
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
     
     
    def test_reminder_create_with_missing_required_fields_does_not_create_reminder(self):
     self.client.login(
        username="viewuser",
        password="Testpass123",
    )

     reminder_count_before = Reminder.objects.count()

     response = self.client.post(
        reverse("reminders:reminder_create"),
        {
            "title": "",
            "reminder_type": "",
            "remind_at": "",
        },
    )

     self.assertEqual(
        response.status_code,
        200,
    )

     self.assertEqual(
        Reminder.objects.count(),
        reminder_count_before,
    )

     self.assertTrue(
        response.context["form"].errors,
    )