from django.contrib import admin

from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "reminder_type",
        "remind_at",
        "is_completed",
    )

    list_filter = (
        "reminder_type",
        "is_completed",
    )

    search_fields = (
        "title",
        "user__username",
    )