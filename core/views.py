from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from applications.models import Application
from companies.models import Company
from interviews.models import Interview
from notes.models import Note


@login_required
def home(request):
    upcoming_interviews = (
        Interview.objects.filter(
            application__user=request.user,
            status="scheduled",
            scheduled_at__gte=timezone.now(),
        )
        .select_related(
            "application",
            "application__company",
        )
        .order_by("scheduled_at")
    )

    recent_companies = Company.objects.filter(
        user=request.user,
    ).order_by(
        "-created_at"
    )[:5]

    recent_applications = (
        Application.objects.filter(
            user=request.user
        )
        .select_related("company")
        .order_by("-application_date")[:5]
    )

    context = {
        "total_companies": Company.objects.filter(
            user=request.user,
        ).count(),
        "total_applications": Application.objects.filter(
            user=request.user
        ).count(),
        "accepted_applications": Application.objects.filter(
            user=request.user,
            status="accepted",
        ).count(),
        "upcoming_interview_count": upcoming_interviews.count(),
        "upcoming_interviews": upcoming_interviews[:5],
        "recent_companies": recent_companies,
        "recent_applications": recent_applications,
    }

    return render(
        request,
        "home.html",
        context,
    )


@login_required
def search_view(request):
    query = request.GET.get("q", "").strip()

    companies = Company.objects.none()
    applications = Application.objects.none()
    interviews = Interview.objects.none()
    notes = Note.objects.none()

    if query:
        companies = Company.objects.filter(
            user=request.user,
        ).filter(
            Q(name__icontains=query)
            | Q(location__icontains=query)
            | Q(website__icontains=query)
        )

        applications = Application.objects.filter(
            user=request.user
        ).filter(
            Q(position__icontains=query)
            | Q(company__name__icontains=query)
            | Q(notes__icontains=query)
        ).select_related("company")

        interviews = Interview.objects.filter(
            application__user=request.user
        ).filter(
            Q(application__position__icontains=query)
            | Q(application__company__name__icontains=query)
            | Q(interviewer_name__icontains=query)
            | Q(location__icontains=query)
            | Q(notes__icontains=query)
        ).select_related(
            "application",
            "application__company",
        )

        notes = Note.objects.filter(
            user=request.user
        ).filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
        )

    context = {
        "query": query,
        "companies": companies,
        "applications": applications,
        "interviews": interviews,
        "notes": notes,
    }

    return render(
        request,
        "core/search_results.html",
        context,
    )