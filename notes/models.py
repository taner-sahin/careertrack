from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Note(models.Model):
    CATEGORY_CHOICES = [
        ("general", "Genel"),
        ("application", "Başvuru"),
        ("interview", "Görüşme"),
        ("learning", "Öğrenme"),
        ("goal", "Hedef"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Düşük"),
        ("medium", "Orta"),
        ("high", "Yüksek"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notes",
    )

    title = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
    )

    content = models.TextField()

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="general",
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    is_pinned = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-is_pinned",
            "-updated_at",
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.user.username}-{self.title}"
            )

        super().save(*args, **kwargs)