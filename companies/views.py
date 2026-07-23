from django.shortcuts import render, redirect
from .forms import CompanyForm


def company_create(request):

    if request.method == "POST":

        form = CompanyForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("home")

    else:

        form = CompanyForm()

    return render(
        request,
        "companies/company_form.html",
        {"form": form},
    )