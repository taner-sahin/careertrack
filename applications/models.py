from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from companies.models import Company


class Application(models.Model):

    STATUS_CHOICES = [
        ("applied", "Başvuruldu"),
        ("interview", "Mülakat"),
        ("rejected", "Reddedildi"),
        ("accepted", "Kabul Edildi"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications",
        null=True,
        blank=True,
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    position = models.CharField(
        max_length=150,
    )

    slug = models.SlugField(
    max_length=220,
    unique=True,
    blank=True,
    null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="applied",
    )

    application_date = models.DateField(
        auto_now_add=True,
    )

    notes = models.TextField(
        blank=True,
    )

    def save(self, *args, **kwargs):

        if not self.slug:

            base_slug = slugify(
                f"{self.company.name}-{self.position}"
            )

            slug = base_slug
            number = 1

            while Application.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{number}"
                number += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company} - {self.position}"