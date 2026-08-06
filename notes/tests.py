from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Note


class NoteViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="noteuser",
            password="Testpass123",
        )

        self.note = Note.objects.create(
            user=self.user,
            title="Django ORM Tekrarı",
            content="filter, get ve all metotlarını tekrar edeceğim.",
            category="learning",
            priority="high",
            is_pinned=True,
        )

        self.other_user = User.objects.create_user(
            username="othernoteuser",
            password="Testpass123",
        )

        self.other_note = Note.objects.create(
            user=self.other_user,
            title="Başka Kullanıcının Notu",
            content="Bu not giriş yapan kullanıcıya görünmemeli.",
            category="general",
            priority="medium",
            is_pinned=False,
        )

    def test_note_list_view(self):
        self.client.login(
            username="noteuser",
            password="Testpass123",
        )

        response = self.client.get(
            reverse("notes:note_list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "notes/note_list.html",
        )

        self.assertContains(
            response,
            "Django ORM Tekrarı",
        )
        
    def test_note_detail_view(self):
     self.client.login(
        username="noteuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse(
            "notes:note_detail",
            kwargs={
                "slug": self.note.slug,
            },
        )
    )

     self.assertEqual(
        response.status_code,
        200,
    )

     self.assertTemplateUsed(
        response,
        "notes/note_detail.html",
    )

     self.assertEqual(
        response.context["note"],
        self.note,
    )

     self.assertContains(
        response,
        "Django ORM Tekrarı",
    )      
        

    def test_note_list_requires_login(self):
     note_list_url = reverse(
        "notes:note_list"
    )

     login_url = reverse(
        "accounts:login"
    )

     response = self.client.get(
        note_list_url
    )

     self.assertRedirects(
        response,
        f"{login_url}?next={note_list_url}",
    )
     
    
    def test_note_list_contains_only_logged_in_users_notes(self):
     self.client.login(
        username="noteuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse("notes:note_list")
    )

     notes = response.context["notes"]

     self.assertIn(
        self.note,
        notes,
    )

     self.assertNotIn(
        self.other_note,
        notes,
    )

     self.assertEqual(
        notes.count(),
        1,
    )
     
    def test_user_cannot_access_other_users_note_detail(self):
     self.client.login(
        username="noteuser",
        password="Testpass123",
    )

     response = self.client.get(
        reverse(
            "notes:note_detail",
            kwargs={
                "slug": self.other_note.slug,
            },
        )
    )

     self.assertEqual(
        response.status_code,
        404,
    )
     
    def test_create_note(self):
     self.client.login(
        username="noteuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse("notes:note_create"),
        {
            "title": "Yeni Test Notu",
            "content": "Bu not test sırasında oluşturuldu.",
            "category": "learning",
            "priority": "medium",
            "is_pinned": True,
        },
    )

     self.assertEqual(
        response.status_code,
        302,
    )

     self.assertTrue(
        Note.objects.filter(
            title="Yeni Test Notu",
            user=self.user,
        ).exists()
    )
     
    def test_update_note(self):
     self.client.login(
        username="noteuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse(
            "notes:note_update",
            kwargs={
                "slug": self.note.slug,
            },
        ),
        {
            "title": "Güncellenmiş Django Notu",
            "content": "ORM sorgularını tekrar ettim.",
            "category": "learning",
            "priority": "medium",
            "is_pinned": False,
        },
    )

     self.assertEqual(
        response.status_code,
        302,
    )

     self.note.refresh_from_db()

     self.assertEqual(
        self.note.title,
        "Güncellenmiş Django Notu",
    )

     self.assertEqual(
        self.note.content,
        "ORM sorgularını tekrar ettim.",
    )

     self.assertEqual(
        self.note.priority,
        "medium",
    )

     self.assertFalse(
        self.note.is_pinned,
    )
     
    def test_delete_note(self):
     self.client.login(
        username="noteuser",
        password="Testpass123",
    )

     response = self.client.post(
        reverse(
            "notes:note_delete",
            kwargs={
                "slug": self.note.slug,
            },
        )
    )

     self.assertEqual(
        response.status_code,
        302,
    )

     self.assertFalse(
        Note.objects.filter(
            slug=self.note.slug,
        ).exists()
    )