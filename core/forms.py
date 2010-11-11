from django import forms
from django.forms.widgets import PasswordInput, Textarea, Select, TextInput

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=100,widget=PasswordInput,required=True)

class ForgotForm(forms.Form):
    destiny = forms.CharField(required=True, label='Username o Email')