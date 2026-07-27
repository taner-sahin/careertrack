from django.urls import path

from . import views


app_name = "applications"

urlpatterns = [

    path(
        "",
        views.application_list,
        name="list",
    ),

    path(
        "create/",
        views.application_create,
        name="create",
    ),

    path(
        "<slug:slug>/update/",
        views.application_update,
        name="update",
    ),

    path(
        "<slug:slug>/",
        views.application_detail,
        name="detail",
    ),
    
    path(
    "<slug:slug>/delete/",
    views.application_delete,
    name="delete",
    ),

]