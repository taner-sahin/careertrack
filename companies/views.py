from django.shortcuts import render, redirect
from .forms import CompanyForm
from .models import Company


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
    
def company_list(request):

    companies = Company.objects.all()

    return render(
        request,
        "companies/company_list.html",
        {"companies": companies},
    )
    
def company_detail(request, slug):

    company = Company.objects.get(
        slug=slug,
    )

    return render(
        request,
        "companies/company_detail.html",
        {"company": company},
    )