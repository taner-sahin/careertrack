from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from companies.models import Company
from applications.models import Application


@login_required
def home(request):
    applications = Application.objects.filter(
        user=request.user,
    )

    total_companies = Company.objects.count()
    total_applications = applications.count()

    accepted_applications = applications.filter(
        status='accepted',
    ).count()

    recent_companies = Company.objects.order_by(
        '-created_at',
    )[:5]

    recent_applications = applications.order_by(
        '-application_date',
    )[:5]

    context = {
        'total_companies': total_companies,
        'total_applications': total_applications,
        'accepted_applications': accepted_applications,
        'recent_companies': recent_companies,
        'recent_applications': recent_applications,
    }

    return render(
        request,
        'home.html',
        context,
    )