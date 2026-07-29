from django.urls import path
from .views import company_create, company_list,  company_detail, company_update, company_delete


app_name = "companies"


urlpatterns = [
    path(
        "create/",
        company_create,
        name="create",
    ),

    path(
        "",
        company_list,
        name="list",
    ),

    path(
        "<slug:slug>/update/",
         company_update,
         name="update",
    ),


    path(
    "<slug:slug>/delete/",
    company_delete,
    name="delete",
    ),
    
    path(
        "<slug:slug>/",
        company_detail,
        name="detail",
    ),
]