from django.contrib.auth.models import User
from django.db import models

from applications.models import Application
from interviews.models import Interview


class Reminder(models.Model):

    REMINDER_TYPE_CHOICES = [
        ("application", "Başvuru"),
        ("interview", "Görüşme"),
        ("cv", "CV"),
        ("other", "Diğer"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reminders",
    )

    title = models.CharField(
        max_length=200,
    )

    reminder_type = models.CharField(
        max_length=20,
        choices=REMINDER_TYPE_CHOICES,
        default="other",
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reminders",
    )

    interview = models.ForeignKey(
        Interview,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reminders",
    )

    remind_at = models.DateTimeField()

    notes = models.TextField(
        blank=True,
    )

    is_completed = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.title