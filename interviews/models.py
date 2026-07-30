from django.db import models

from applications.models import Application


class Interview(models.Model):
    INTERVIEW_TYPE_CHOICES = [
        ("hr", "İnsan Kaynakları Görüşmesi"),
        ("technical", "Teknik Görüşme"),
        ("manager", "Yönetici Görüşmesi"),
        ("final", "Final Görüşmesi"),
        ("other", "Diğer"),
    ]

    STATUS_CHOICES = [
        ("scheduled", "Planlandı"),
        ("completed", "Tamamlandı"),
        ("cancelled", "İptal Edildi"),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="interviews",
    )
    interview_type = models.CharField(
        max_length=20,
        choices=INTERVIEW_TYPE_CHOICES,
    )
    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled",
    )
    location = models.CharField(
        max_length=255,
        blank=True,
    )
    meeting_link = models.URLField(
        blank=True,
    )
    interviewer_name = models.CharField(
        max_length=150,
        blank=True,
    )
    notes = models.TextField(
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["scheduled_at"]

    def __str__(self):
        return (
            f"{self.application.company.name} - "
            f"{self.get_interview_type_display()}"
        )