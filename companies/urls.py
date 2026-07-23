from django.urls import path
from .views import company_create

urlpatterns = [
    path("create/", company_create, name="company_create"),
]