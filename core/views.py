from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from companies.models import Company
from applications.models import Application

from django.utils import timezone

from interviews.models import Interview

@login_required
def home(request):
    upcoming_interviews = Interview.objects.filter(
        application__user=request.user,
        status="scheduled",
        scheduled_at__gte=timezone.now(),
    ).select_related(
        "application",
        "application__company",
    ).order_by("scheduled_at")

    recent_companies = Company.objects.order_by("-created_at")[:5]

    recent_applications = (
        Application.objects
        .filter(user=request.user)
        .select_related("company")
        .order_by("-application_date")[:5]
    )

    context = {
        "total_companies": Company.objects.count(),
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

    return render(request, "home.html", context)
    upcoming_interviews = Interview.objects.filter(
        application__user=request.user,
        status="scheduled",
        scheduled_at__gte=timezone.now(),
    ).select_related(
        "application",
        "application__company",
    ).order_by("scheduled_at")

    context = {
        "total_companies": Company.objects.count(),
        "total_applications": Application.objects.filter(
            user=request.user
        ).count(),
        "accepted_applications": Application.objects.filter(
            user=request.user,
            status="accepted",
        ).count(),
        "upcoming_interview_count": upcoming_interviews.count(),
        "upcoming_interviews": upcoming_interviews[:5],
    }

    return render(request, "home.html", context)