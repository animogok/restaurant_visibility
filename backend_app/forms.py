from django import forms
from django.contrib.auth.models import User

'''
This class is responsible for managing the forms on the API endpoints, also it is using the ModelForm due to the available of working directly with the database model instance
making easy the way we control de information coming from the frontend
'''

#Register setting form, this will allow and easy way to created the register form
class User_Registration(forms.Form):
    username = forms.CharField(required=True, max_length=150, widget=forms.TextInput({'placeholder' : 'set your username'}))
    first_name = forms.CharField(required=True, max_length=150, widget=forms.TextInput)
    last_name = forms.CharField(required=True, max_length=150, widget=forms.TextInput)
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)
