from django import forms

from .models import Reminder


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = [
            "title",
            "reminder_type",
            "application",
            "interview",
            "remind_at",
            "notes",
            "is_completed",
        ]

        widgets = {
            "remind_at": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields["application"].queryset = (
                self.fields["application"]
                .queryset.filter(
                    user=user,
                )
                .select_related("company")
            )

            self.fields["interview"].queryset = (
                self.fields["interview"]
                .queryset.filter(
                    application__user=user,
                )
                .select_related(
                    "application",
                    "application__company",
                )
            )