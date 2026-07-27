from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm
from .models import Application


@login_required
def application_list(request):

    applications = Application.objects.filter(
        user=request.user
    ).order_by("-application_date")

    context = {
        "applications": applications,
    }

    return render(
        request,
        "applications/application_list.html",
        context,
    )


@login_required
def application_create(request):

    if request.method == "POST":

        form = ApplicationForm(request.POST)

        if form.is_valid():

            application = form.save(commit=False)

            application.user = request.user

            application.save()

            return redirect("applications:list")

    else:

        form = ApplicationForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "applications/application_form.html",
        context,
    )


@login_required
def application_detail(request, slug):

    application = get_object_or_404(
        Application,
        slug=slug,
        user=request.user,
    )

    context = {
        "application": application,
    }

    return render(
        request,
        "applications/application_detail.html",
        context,
    )
    
@login_required
def application_update(request, slug):

    application = get_object_or_404(
        Application,
        slug=slug,
        user=request.user,
    )

    if request.method == "POST":

        form = ApplicationForm(
            request.POST,
            instance=application,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "applications:detail",
                slug=application.slug,
            )

    else:

        form = ApplicationForm(
            instance=application,
        )

    context = {
        "form": form,
        "application": application,
    }

    return render(
        request,
        "applications/application_update.html",
        context,
    )
    
@login_required
def application_delete(request, slug):

    application = get_object_or_404(
        Application,
        slug=slug,
        user=request.user,
    )

    if request.method == "POST":

        application.delete()

        return redirect("applications:list")

    context = {
        "application": application,
    }

    return render(
        request,
        "applications/application_delete.html",
        context,
    )