from django import forms
from django.forms import ModelForm, PasswordInput, Textarea, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Keyword,Profile
from django.core.files.images import get_image_dimensions

form_control_class = forms.TextInput(attrs={'class': 'form-control'})

class SignUpForm(UserCreationForm):
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
        exclude = ['alert_name', 'User', 'optional_keywords', 'excluded_keywords', 'required_keywords']

class KeywordForm_One(ModelForm):
    class Meta:
        model = Keyword
        fields = ['alert_name', 'optional_keywords']
        widgets = {
            'alert_name': TextInput(attrs={'placeholder': 'Here we are', 'type': 'hidden'}),
            'optional_keywords': Textarea(attrs={'placeholder': 'add optional keyword here'}),

        }

class ContactForm(forms.Form):
    email_address = forms.EmailField(max_length=254, widget=form_control_class)
    subject=forms.CharField(max_length=500, required=True, widget=form_control_class)
    message = forms.CharField(required=True,widget=forms.Textarea)

    class Meta:
        model = Keyword
        fields = ['email_address', 'subject', 'message']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['id', 'bio', 'location', 'email_confirmed', 'user_id']

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 1000
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                            'GIF or PNG image.')

            # validate file size
            if len(avatar) > (5000 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 2000k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar

class UserEditForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']