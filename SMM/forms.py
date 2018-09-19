from django import forms
from django.forms import ModelForm, PasswordInput, Textarea, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Keyword


class SignUpForm(UserCreationForm):
    form_control_class = forms.TextInput(attrs={'class': 'form-control'})
    username = forms.CharField(max_length=30, required=True, widget=form_control_class)
    first_name = forms.CharField(max_length=30, required=True, widget=form_control_class)
    last_name = forms.CharField(max_length=30, required=True, widget=form_control_class)
    email = forms.EmailField(max_length=254, widget=form_control_class)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'New password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Conform password',}),help_text="Enter the same password as before, for verification.")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

class KeywordForm(ModelForm):
    class Meta:
        model = Keyword
        exclude = ['alert_name', 'Userid', 'optional_keywords', 'excluded_keywords', 'required_keywords']

class KeywordForm_One(ModelForm):
    class Meta:
        model = Keyword
        fields = ['alert_name', 'optional_keywords']
        widgets = {
            'alert_name': TextInput(attrs={'placeholder': 'Here we are', 'type': 'hidden'}),
            'optional_keywords': Textarea(attrs={'placeholder': 'add optional keyword here'}),

        }
