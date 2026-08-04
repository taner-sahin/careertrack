from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note

        fields = [
            "title",
            "content",
            "category",
            "priority",
            "is_pinned",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Not başlığını yazın",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 7,
                    "placeholder": "Kariyer sürecinizle ilgili notunuzu yazın",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "priority": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "is_pinned": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }