from django.forms import ModelForm
from django.contrib.auth.models import User

'''
This class is responsible for managing the forms on the API endpoints, also it is using the ModelForm due to the available of working directly with the database model instance
making easy the way we control de information coming from the frontend
'''

#Register setting form

class User_Registration(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']