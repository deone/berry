from django import forms
from django.contrib.auth.forms import AuthenticationForm

from refer.forms import DivErrorList

class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
	super(AuthForm, self).__init__(*args, **kwargs)

	self.error_class = DivErrorList
	self.fields['username'].label = "Phone Number"
	self.fields['username'].widget = forms.TextInput(attrs={'class':
	    'integer', 'maxlength': 11})
