#!/usr/bin/env python
from django import forms
from django.forms.widgets import PasswordInput, TextInput, Textarea
from how2.core.models import How2, Category

class ProfileForm(forms.Form):
    username = forms.CharField(max_length=30,required=False)
    password = forms.CharField(max_length=30,required=False, widget=PasswordInput)
    firstname = forms.CharField(max_length=100,required=False)
    lastname = forms.CharField(max_length=100,required=False)
    email = forms.EmailField(required=False)
    image = forms.ImageField(label="Avatar",required=False)
    birthday = forms.DateField(label="Fecha de nacimiento",required=False)
    country = forms.CharField(label="Pais", max_length=100,required=False)
    state = forms.CharField(label="Estado", max_length=100,required=False)
    city = forms.CharField(label="Ciudad", max_length=100,required=False)
    role = forms.CharField(label="Ocupacion", max_length=100,required=False)
    interest = forms.CharField(label="Intereses", widget=Textarea,required=False)

class How2Form(forms.ModelForm):
    title = forms.CharField(initial='Como', widget= TextInput(attrs={'size':'50'}))
    class Meta:
        model = How2
        fields = ('title','category','content')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('is_active')