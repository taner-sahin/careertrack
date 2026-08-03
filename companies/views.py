from django.shortcuts import get_object_or_404, redirect, render

from .forms import CompanyForm
from .models import Company


def company_create(request):

    if request.method == "POST":

        form = CompanyForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("core:home")

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
    
def company_update(request, slug):
    company = get_object_or_404(
        Company,
        slug=slug,
    )

    if request.method == "POST":
        form = CompanyForm(
            request.POST,
            instance=company,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "companies:detail",
                slug=company.slug,
            )

    else:
        form = CompanyForm(
            instance=company,
        )

    context = {
        "form": form,
        "company": company,
    }

    return render(
        request,
        "companies/company_form.html",
        context,
    )
    
def company_delete(request, slug):
    company = get_object_or_404(
        Company,
        slug=slug,
    )

    if request.method == "POST":
        company.delete()

        return redirect(
            "companies:list",
        )

    context = {
        "company": company,
    }

    return render(
        request,
        "companies/company_confirm_delete.html",
        context,
    )