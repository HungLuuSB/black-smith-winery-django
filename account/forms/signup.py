from django import forms
from django.forms import models, widgets
from django.contrib.auth.forms import UserCreationForm
from account.models import CustomUser


class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'full_name', 'phone', 'address', 'city')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user
