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
    

        