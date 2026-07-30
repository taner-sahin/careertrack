from django.urls import path

from . import views


app_name = "interviews"


urlpatterns = [
    path(
        "",
        views.interview_list,
        name="interview_list",
    ),
    path(
        "add/",
        views.interview_create,
        name="interview_create",
    ),
    path(
        "<int:pk>/",
        views.interview_detail,
        name="interview_detail",
    ),
    path(
        "<int:pk>/edit/",
        views.interview_update,
        name="interview_update",
    ),
    path(
        "<int:pk>/delete/",
        views.interview_delete,
        name="interview_delete",
    ),
]