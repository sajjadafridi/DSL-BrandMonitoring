from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, PasswordInput, Textarea, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Keyword, Profile, COMPANY_SIZE
from django.utils.safestring import mark_safe
from django.core.files.images import get_image_dimensions
from string import Template

form_control_class = forms.TextInput(attrs={'class': 'form-control'})


class AuthenticationRememberMeForm(AuthenticationForm):

    """
    Subclass of Django ``AuthenticationForm`` which adds a remember me
    checkbox.

    """

    remember_me = forms.BooleanField(label=_('Remember Me'), initial=False,
                                     required=False)


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        html = Template("""<img src="$link"/>""")
        return mark_safe(html.substitute(link=value))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=30, required=True, widget=form_control_class, help_text="user name and email should be unique.")
    first_name = forms.CharField(
        max_length=30, required=True, widget=form_control_class)
    last_name = forms.CharField(
        max_length=30, required=True, widget=form_control_class)
    email = forms.EmailField(max_length=254, widget=form_control_class)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Conform password', }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)


class KeywordForm(ModelForm):
    class Meta:
        model = Keyword
        exclude = ['alert_name', 'User']


class ContactForm(forms.Form):
    email_address = forms.EmailField(max_length=254, widget=form_control_class)
    subject = forms.CharField(
        max_length=500, required=True, widget=form_control_class)
    message = forms.CharField(required=True, widget=forms.Textarea)

    class Meta:
        model = Keyword
        fields = ['email_address', 'subject', 'message']


class UserProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(label=('Profile Image'), required=False, error_messages={
                                     'invalid': ("Image files only")}, widget=forms.FileInput)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['company_size'] = forms.ChoiceField(
                choices=COMPANY_SIZE, widget=forms.Select(attrs={'class': 'form-control'}))
            self.fields['company_name'] = forms.CharField(
                widget=form_control_class, required=False)

    class Meta:
        model = Profile
        exclude = ['id', 'bio', 'location', 'email_confirmed', 'user_id',
                   'user', 'phone_number', 'country', 'birth_date', 'full_name', 'email']

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
    email = forms.EmailField(
        required=True, widget=form_control_class, disabled=True)
    first_name = forms.CharField(required=False, widget=form_control_class)
    last_name = forms.CharField(required=False, widget=form_control_class)

    class Meta:
        model = User
        exclude = ['username']
        fields = ['first_name', 'last_name', 'email']


class RemoveUser(forms.Form):
    username = forms.CharField(widget=forms.HiddenInput(), required=False)
