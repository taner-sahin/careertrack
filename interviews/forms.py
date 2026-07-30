from django import forms

from .models import Interview


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview

        fields = [
            "application",
            "interview_type",
            "scheduled_at",
            "status",
            "location",
            "meeting_link",
            "interviewer_name",
            "notes",
        ]

        widgets = {
            "scheduled_at": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ofis adresi veya online görüşme",
                }
            ),
            "meeting_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://...",
                }
            ),
            "interviewer_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Görüşmeci adı",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Mülakat hazırlık notları",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        self.fields["application"].widget.attrs.update(
            {"class": "form-select"}
        )

        self.fields["interview_type"].widget.attrs.update(
            {"class": "form-select"}
        )

        self.fields["status"].widget.attrs.update(
            {"class": "form-select"}
        )

        if user:
            self.fields["application"].queryset = (
                self.fields["application"]
                .queryset
                .filter(user=user)
                .select_related("company")
            )