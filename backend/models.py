from django.db import models
from django.contrib.auth.models import User

'''
For user database model, I will been using user.model from django, for the next reasons: have the data for managing the user easly and freely
also django provides me methods for the actual posting of the information and security parameters, moreover django provides classes who might help
in terms of authentication.

For other database models, I will create its models right below this comments because it is outside other user management and I can connect them
using foreign keys.
'''

#This class will be related by a foreign key to the user instance who created the admin-account.
class RestaurantInfo_DBModel(models.Model):
    user_Instance = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=100)
    restaurant_address = models.CharField(max_length=254)
    restaurant_staffOwner = models.BooleanField(default=True)
    restaurant_subStaffOwner = models.BooleanField(default=False)
    restaurant_reservations = models.BooleanField(default=False)
    
    #This field it's for managing the amount of admin_lvl2 of every restaurant
    restaurant_subStaffOwner_Q = models.IntegerField(default=0)
    
    #This method will be called everytime the main admin desires to add numbers of subStaffs up 
    def addUp_subStaff_Q(self, id_restaurant : int) -> None:
        
        #We get the field to validate if theres is any other subStaff. If the result equals to False we set the camp to True making reference at the first subStaff
        if RestaurantInfo_DBModel.objects.get(id = id_restaurant).restaurant_subStaffOwner == False:
            RestaurantInfo_DBModel.objects.filter(id = id_restaurant).update(estaurant_subStaffOwner = True)
        
        Q_subStaff =  RestaurantInfo_DBModel.objects.get(id = id_restaurant).restaurant_subStaffOwner_Q
        
        RestaurantInfo_DBModel.objects.filter(id = id_restaurant).update(restaurant_subStaffOwner_Q = (Q_subStaff + 1))
        
#This class will be related to an instance of one created account that have a reference with a restaurant
#Will comprehend an user with admin-lvl#2
class Admin_lvl1(models.Model):
    user_Instance = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_Instacen = models.ForeignKey(RestaurantInfo_DBModel, on_delete=models.CASCADE)
