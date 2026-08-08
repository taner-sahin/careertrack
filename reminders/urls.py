from django.urls import path

from . import views


app_name = "reminders"


urlpatterns = [
    path(
        "",
        views.reminder_list,
        name="reminder_list",
    ),
    path(
        "add/",
        views.reminder_create,
        name="reminder_create",
    ),
    path(
        "<int:pk>/",
        views.reminder_detail,
        name="reminder_detail",
    ),
    path(
        "<int:pk>/edit/",
        views.reminder_update,
        name="reminder_update",
    ),
    path(
        "<int:pk>/delete/",
        views.reminder_delete,
        name="reminder_delete",
    ),
]