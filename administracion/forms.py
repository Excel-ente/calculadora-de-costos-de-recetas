from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = True
        
        if commit:
            user.save()

        return user


class RecetaSearchForm(forms.Form):
    nombre = forms.CharField(required=False, label='Nombre de la receta')
    usuario = forms.CharField(required=False, label='Nombre de usuario')
