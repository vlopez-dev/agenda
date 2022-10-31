from dataclasses import field
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Requerido .254 carácteres como máximo y debe ser un email válido.",
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password1")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column("username", css_class="form-control form-control-user"),
            Column("password", css_class="form-control form-control-user"),
        )
