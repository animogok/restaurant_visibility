from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from restaurant_info import settings
from .models import RestaurantInfo_DBModel

'''
Here will be the logic related to the authentication that holds actions related to the staff admin of every restaurant page.

    Restaurant Registration Group (RRG)
        ACTIONS
            - Allow the basic CRUD management of db instance that owns the restaurant
            - Allow the control of the information related to the user that created the restaurant site
            - Allow the protection of the User data
'''
RRGpermission_list = [
    'create_restaurantInformation',
    'reade_restaurantInformation',
    'update_restaurantInformation',
    'delete_restaurantInformation'
]

def create_or_get_RRG():
    group_RRG, created = Group.objects.get_or_create(name='Restaurant Registration Group')
    permissions = Permission.objects.filter(content_type = ContentType.objects.get_for_model(RestaurantInfo_DBModel), codename__in=RRGpermission_list)
    group_RRG.permissions.set(permissions)
    

'''
This class will be taking care of a simple email verification via six_digit_number.

This will using two simple methods, one of the methods will generate the code and other information, moreover the second method will
validate the data by making use of the current time and the max expiration time, if it's true, the field in bd that specifies the email verification, will be on True
'''

import random
from datetime import timedelta,datetime

from .models import UserVerification
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from hashid_field import Hashid

CURRENT_TIME = datetime.now()

class Six_digit_Gen_Val:
    h = Hashid(settings.hash_field_salt)
    code =random.randint(100000, 999999)
    
    def generator(self):
        values = {
            'six_digits_code' : str(self.h.encode(id=self.code)),
            'current_time' : str(CURRENT_TIME.strftime("%d,%m,%H,%M")),
            'exp_time' : str((CURRENT_TIME + timedelta(minutes=5))).strftime("%d,%m,%H,%M")
        }
  
        return values
        
    def validator(self, values : dict, user_id : int):

        if (CURRENT_TIME) >= values.get("exp_time"):
            raise ValidationError
        
        else:
            user_email_camp = get_object_or_404(UserVerification, user = user_id)
            user_email_camp.email_verification = True
            user_email_camp.asave()

hola = Six_digit_Gen_Val()
print(hola.generator())