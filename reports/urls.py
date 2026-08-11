from django.urls import path

from . import views


app_name = "reports"


urlpatterns = [
    path(
        "",
        views.report_dashboard,
        name="report_dashboard",
    ),
    
    path(
    "export/applications/csv/",
    views.export_applications_csv,
    name="export_applications_csv",
    ), 
    
    path(
    "export/applications/pdf/",
    views.export_applications_pdf,
    name="export_applications_pdf",
    ),
    
]