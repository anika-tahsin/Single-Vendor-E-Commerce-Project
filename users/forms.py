from .models import customerUser

from django.contrib.auth.forms import UserCreationForm
from django import forms

class customUserRegistrationForm(UserCreationForm):
    fullname = forms.CharField(max_length=100, required=True, help_text="Enter your fullname")

    class Meta:
        model = customerUser
        fields = ["fullname", "email", "password1", "password2"]

    def save(self,commit=True):
        user = super().save(commit=False)
        fullname = self.cleaned_data.get("fullname", "")
        name_parts = fullname.strip().split(" ", 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ""
        if commit:
            user.save()
        return user