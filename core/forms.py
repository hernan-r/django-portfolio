from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Formulario público de contacto con protección anti-spam simple."""

    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "hp-field",
                "tabindex": "-1",
                "autocomplete": "off",
                "aria-hidden": "true",
            }
        ),
        label="",
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "company", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Tu nombre",
                    "autocomplete": "name",
                    "class": "field-input",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "tu@email.com",
                    "autocomplete": "email",
                    "class": "field-input",
                }
            ),
            "company": forms.TextInput(
                attrs={
                    "placeholder": "Empresa (opcional)",
                    "autocomplete": "organization",
                    "class": "field-input",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "placeholder": "¿Sobre qué querés hablar?",
                    "class": "field-input",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Contame sobre la oportunidad, el proyecto o la consulta…",
                    "rows": 6,
                    "class": "field-input field-textarea",
                }
            ),
        }
        labels = {
            "name": "Nombre",
            "email": "Email",
            "company": "Empresa",
            "subject": "Asunto",
            "message": "Mensaje",
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Ingresá tu nombre completo.")
        return name

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 20:
            raise forms.ValidationError(
                "Contame un poco más: el mensaje debe tener al menos 20 caracteres."
            )
        return message

    def clean_website(self):
        website = self.cleaned_data.get("website", "")
        if website:
            raise forms.ValidationError("No pudimos validar el formulario.")
        return website
