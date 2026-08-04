from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "category",
        "priority",
        "is_pinned",
        "updated_at",
    )

    list_filter = (
        "category",
        "priority",
        "is_pinned",
        "created_at",
    )

    search_fields = (
        "title",
        "content",
        "user__username",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-is_pinned",
        "-updated_at",
    )