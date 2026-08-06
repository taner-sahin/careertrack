from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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

    context = {
        "total_applications": applications.count(),
        "accepted_applications": applications.filter(
            status="accepted",
        ).count(),
        "rejected_applications": applications.filter(
            status="rejected",
        ).count(),
        "interview_applications": applications.filter(
            status="interview",
        ).count(),

        "total_interviews": interviews.count(),
        "scheduled_interviews": interviews.filter(
            status="scheduled",
        ).count(),
        "completed_interviews": interviews.filter(
            status="completed",
        ).count(),

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