from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import AccountSettingsForm


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            login(request, user)

            return redirect("home")

    return render(request, "login.html")


def register_view(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("accounts:login")

    else:

        form = UserCreationForm()

    context = {
        "form": form,
    }

    return render(request, "register.html", context)


def logout_view(request):

    logout(request)

    return redirect("accounts:login")

@login_required
def settings_view(request):
    if request.method == "POST":
        form = AccountSettingsForm(
            request.POST,
            instance=request.user,
        )

        if form.is_valid():
            form.save()
            return redirect("accounts:settings")

    else:
        form = AccountSettingsForm(
            instance=request.user,
        )

    return render(
        request,
        "accounts/account_settings.html",
        {
            "form": form,
        },
    )