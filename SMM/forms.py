from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
	form_control_class=forms.TextInput(attrs={'class':'form-control'})
	username = forms.CharField(max_length=30, required=False,widget =form_control_class )
	first_name = forms.CharField(max_length=30, required=False,widget =form_control_class )
	last_name = forms.CharField(max_length=30, required=False, widget =form_control_class )
	email = forms.EmailField(max_length=254, help_text='Required',widget =form_control_class )
	password1 = forms.CharField(widget = forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)

	# company_name = forms.CharField(max_length=30, required=False, widget =form_control_class )
	# show_password = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'text-left'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
		# fields = ('first_name', 'last_name', 'company_name','email','password1','password2','show_password',)
class keyword_model(forms.Form):
	serch = forms.CharField(max_length=200,required=True)
	class Meta:
		model=forms
		fields = ('search_keyword')