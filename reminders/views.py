from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReminderForm
from .models import Reminder


@login_required
def reminder_list(request):
    reminders = Reminder.objects.filter(
        user=request.user
    ).order_by("remind_at")

    return render(
        request,
        "reminders/reminder_list.html",
        {
            "reminders": reminders,
        },
    )


@login_required
def reminder_detail(request, pk):
    reminder = get_object_or_404(
        Reminder,
        pk=pk,
        user=request.user,
    )

    return render(
        request,
        "reminders/reminder_detail.html",
        {
            "reminder": reminder,
        },
    )


@login_required
def reminder_create(request):
    if request.method == "POST":
        form = ReminderForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()

            return redirect(
                "reminders:reminder_list"
            )

    else:
        form = ReminderForm(
            user=request.user,
        )

    return render(
        request,
        "reminders/reminder_form.html",
        {
            "form": form,
            "page_title": "Yeni Hatırlatıcı",
        },
    )


@login_required
def reminder_update(request, pk):
    reminder = get_object_or_404(
        Reminder,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        form = ReminderForm(
            request.POST,
            instance=reminder,
            user=request.user,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "reminders:reminder_detail",
                pk=reminder.pk,
            )

    else:
        form = ReminderForm(
            instance=reminder,
            user=request.user,
        )

    return render(
        request,
        "reminders/reminder_form.html",
        {
            "form": form,
            "page_title": "Hatırlatıcıyı Güncelle",
        },
    )


@login_required
def reminder_delete(request, pk):
    reminder = get_object_or_404(
        Reminder,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        reminder.delete()

        return redirect(
            "reminders:reminder_list"
        )

    return render(
        request,
        "reminders/reminder_confirm_delete.html",
        {
            "reminder": reminder,
        },
    )