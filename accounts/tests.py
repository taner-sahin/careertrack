from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountSettingsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="settingsuser",
            password="Testpass123",
            email="settings@example.com",
        )

    def test_settings_page_opens_for_logged_in_user(self):
        self.client.login(
            username="settingsuser",
            password="Testpass123",
        )

        response = self.client.get(
            reverse("accounts:settings")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "accounts/account_settings.html",
        )
        
    def test_settings_page_requires_login(self):
     settings_url = reverse(
        "accounts:settings"
    )

     login_url = reverse(
        "accounts:login"
    )

     response = self.client.get(
        settings_url
    )

     self.assertRedirects(
        response,
        f"{login_url}?next={settings_url}",
    )
     
    def test_settings_form_contains_current_user_data(self):
     self.user.first_name = "Taner"
     self.user.last_name = "Şahin"
     self.user.save()

     self.client.login(
        username="settingsuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("accounts:settings")
    )

     form = response.context["form"]

     self.assertEqual(
        form.instance,
        self.user,
    )

     self.assertEqual(
        form.initial["username"],
        "settingsuser",
    )

     self.assertEqual(
        form.initial["first_name"],
        "Taner",
    )

     self.assertEqual(
        form.initial["last_name"],
        "Şahin",
    )

     self.assertEqual(
        form.initial["email"],
        "settings@example.com",
    )
     
    def test_user_can_update_account_settings(self):
     self.client.login(
        username="settingsuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse("accounts:settings"),
        {
            "username": "newsettingsuser",
            "first_name": "Taner",
            "last_name": "Şahin",
            "email": "new@example.com",
        },
    )

     self.assertEqual(
        response.status_code,
        302,
    )

     self.user.refresh_from_db()

     self.assertEqual(
        self.user.username,
        "newsettingsuser",
    )

     self.assertEqual(
        self.user.first_name,
        "Taner",
    )

     self.assertEqual(
        self.user.last_name,
        "Şahin",
    )

     self.assertEqual(
        self.user.email,
        "new@example.com",
    )
     
    def test_account_settings_form_rejects_empty_username(self):
     self.client.login(
        username="settingsuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse("accounts:settings"),
        {
            "username": "",
            "first_name": "Taner",
            "last_name": "Şahin",
            "email": "settings@example.com",
        },
    )

     self.assertEqual(
        response.status_code,
        200,
    )

     form = response.context["form"]

     self.assertFalse(
        form.is_valid()
    )

     self.assertIn(
        "username",
        form.errors,
    )

     self.user.refresh_from_db()

     self.assertEqual(
        self.user.username,
        "settingsuser",
    )
     
def test_updating_settings_does_not_change_other_user(self):
    other_user = User.objects.create_user(
        username="otheruser",
        password="Otherpass123",
        email="other@example.com",
    )

    self.client.login(
        username="settingsuser",
        password="Testpass123",
    )

    response = self.client.post(
        reverse("accounts:settings"),
        {
            "username": "updatedsettingsuser",
            "first_name": "Taner",
            "last_name": "Şahin",
            "email": "updated@example.com",
        },
    )

    self.assertEqual(
        response.status_code,
        302,
    )

    other_user.refresh_from_db()

    self.assertEqual(
        other_user.username,
        "otheruser",
    )

    self.assertEqual(
        other_user.email,
        "other@example.com",
    )