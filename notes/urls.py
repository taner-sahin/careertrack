from django.urls import path

from . import views


app_name = "notes"


urlpatterns = [
    path(
        "",
        views.note_list,
        name="note_list",
    ),
    path(
        "add/",
        views.note_create,
        name="note_create",
    ),
    path(
        "<slug:slug>/",
        views.note_detail,
        name="note_detail",
    ),
    path(
        "<slug:slug>/edit/",
        views.note_update,
        name="note_update",
    ),
    path(
        "<slug:slug>/delete/",
        views.note_delete,
        name="note_delete",
    ),
]