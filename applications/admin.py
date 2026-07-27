from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "company",
        "position",
        "status",
        "application_date",
        
    )

    list_filter = (
        "status",
        "application_date",
    )

    search_fields = (
        "company__name",
        "position",
    )

    prepopulated_fields = {}