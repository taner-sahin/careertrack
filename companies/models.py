from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Company(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="companies",
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=200,
    )

    website = models.URLField(
        blank=True,
        null=True,
    )

    location = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):

        return self.name