from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["name", "number", "email", "curso"]

        widgets = {
            "name": forms.TextInput(attrs={
                "id": "name",
                "placeholder": "Ex: David Silva",
                "required": True,
            }),
            "number": forms.TextInput(attrs={
                "id": "number",
                "placeholder": "Ex: 11999999999",
                "required": True,
                "inputmode": "tel",
            }),
            "email": forms.EmailInput(attrs={
                "id": "email",
                "placeholder": "voce@email.com",
            }),
            "curso": forms.TextInput(attrs={
                "id": "curso",
                "placeholder": "Ex: Administração / Pós Injetáveis",
                "required": True,
            }),
        }

    def clean_number(self):
        raw = self.cleaned_data.get("number", "")
        digits = "".join(ch for ch in raw if ch.isdigit())

        # aceita 10 ou 11 dígitos (DDD + número)
        if len(digits) not in (10, 11):
            raise forms.ValidationError("Digite um WhatsApp válido (DDD + número).")

        return digits
