from django import forms
from .models import *


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'password1']
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')
        if password != password1:
            raise forms.ValidationError("Passwords must match")
        
class PasswordResetEmail(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user with this email found")
        return email