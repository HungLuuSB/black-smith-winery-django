from django import forms

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)