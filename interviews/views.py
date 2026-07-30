from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import InterviewForm
from .models import Interview


@login_required
def interview_list(request):
    interviews = (
        Interview.objects
        .filter(application__user=request.user)
        .select_related("application", "application__company")
        .order_by("scheduled_at")
    )

    context = {
        "interviews": interviews,
    }

    return render(
        request,
        "interviews/interview_list.html",
        context,
    )


@login_required
def interview_detail(request, pk):
    interview = get_object_or_404(
        Interview.objects.select_related(
            "application",
            "application__company",
        ),
        pk=pk,
        application__user=request.user,
    )

    context = {
        "interview": interview,
    }

    return render(
        request,
        "interviews/interview_detail.html",
        context,
    )


@login_required
def interview_create(request):
    if request.method == "POST":
        form = InterviewForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            form.save()

            return redirect("interviews:interview_list")

    else:
        form = InterviewForm(user=request.user)

    context = {
        "form": form,
    }

    return render(
        request,
        "interviews/interview_form.html",
        context,
    )


@login_required
def interview_update(request, pk):
    interview = get_object_or_404(
        Interview,
        pk=pk,
        application__user=request.user,
    )

    if request.method == "POST":
        form = InterviewForm(
            request.POST,
            instance=interview,
            user=request.user,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "interviews:interview_detail",
                pk=interview.pk,
            )

    else:
        form = InterviewForm(
            instance=interview,
            user=request.user,
        )

    context = {
        "form": form,
        "interview": interview,
    }

    return render(
        request,
        "interviews/interview_form.html",
        context,
    )


@login_required
def interview_delete(request, pk):
    interview = get_object_or_404(
        Interview,
        pk=pk,
        application__user=request.user,
    )

    if request.method == "POST":
        interview.delete()

        return redirect("interviews:interview_list")

    context = {
        "interview": interview,
    }

    return render(
        request,
        "interviews/interview_confirm_delete.html",
        context,
    )