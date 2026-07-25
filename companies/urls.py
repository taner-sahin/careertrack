from django.urls import path
from .views import company_create, company_list,  company_detail


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
    "<slug:slug>/",
    company_detail,
    name="detail",
   ),
]