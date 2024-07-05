from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

'''
This class will serialize the user model data for managing the upcomings JWT tokens using the library "djangorestframework-simplejwt".
The principal use it's for save the data that the code would be using for the email validations.
'''

class UserDataSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','password']