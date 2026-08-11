import csv
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from applications.models import Application
from interviews.models import Interview
from notes.models import Note


@login_required
def report_dashboard(request):
    applications = Application.objects.filter(
        user=request.user,
    )

    interviews = Interview.objects.filter(
        application__user=request.user,
    )

    notes = Note.objects.filter(
        user=request.user,
    )

    total_applications = applications.count()

    accepted_applications = applications.filter(
        status="accepted",
    ).count()

    rejected_applications = applications.filter(
        status="rejected",
    ).count()

    interview_applications = applications.filter(
        status="interview",
    ).count()

    total_interviews = interviews.count()

    scheduled_interviews = interviews.filter(
        status="scheduled",
    ).count()

    completed_interviews = interviews.filter(
        status="completed",
    ).count()

    if total_applications > 0:
        acceptance_rate = round(
            (accepted_applications / total_applications) * 100,
            1,
        )
    else:
        acceptance_rate = 0

    if total_applications > 0:
        interview_rate = round(
            (interview_applications / total_applications) * 100,
            1,
        )
    else:
        interview_rate = 0

    if total_applications > 0:
        rejection_rate = round(
            (rejected_applications / total_applications) * 100,
            1,
        )
    else:
        rejection_rate = 0

    if total_interviews > 0:
        interview_completion_rate = round(
            (completed_interviews / total_interviews) * 100,
            1,
        )
    else:
        interview_completion_rate = 0

    thirty_days_ago = (
        timezone.now().date() - timedelta(days=30)
    )

    recent_applications = applications.filter(
        application_date__gte=thirty_days_ago,
    ).count()

    company_application_counts = (
        applications
        .values("company__name")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    top_company = company_application_counts.first()

    context = {
        "total_applications": total_applications,
        "accepted_applications": accepted_applications,
        "rejected_applications": rejected_applications,
        "interview_applications": interview_applications,
        "acceptance_rate": acceptance_rate,
        "interview_rate": interview_rate,
        "rejection_rate": rejection_rate,
        "recent_applications": recent_applications,
        "top_company": top_company,

        "total_interviews": total_interviews,
        "scheduled_interviews": scheduled_interviews,
        "completed_interviews": completed_interviews,
        "interview_completion_rate": interview_completion_rate,

        "total_notes": notes.count(),
        "high_priority_notes": notes.filter(
            priority="high",
        ).count(),
        "pinned_notes": notes.filter(
            is_pinned=True,
        ).count(),
    }

    return render(
        request,
        "reports/report_dashboard.html",
        context,
    )


@login_required
def export_applications_csv(request):
    applications = Application.objects.filter(
        user=request.user,
    )

    response = HttpResponse(
        content_type="text/csv; charset=utf-8"
    )

    response.write("\ufeff")

    response["Content-Disposition"] = (
        'attachment; filename="applications.csv"'
    )

    writer = csv.writer(
        response,
        delimiter=";",
    )

    writer.writerow([
        "Company",
        "Position",
        "Status",
        "Application Date",
    ])

    for application in applications:
        writer.writerow([
            application.company.name,
            application.position,
            application.get_status_display(),
            application.application_date,
        ])

    return response