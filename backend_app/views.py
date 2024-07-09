from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views import View
from django.utils.decorators import method_decorator
from asgiref.sync import sync_to_async

from hashids import Hashids

from backend_app.models import UserVerification
from restaurant_info import settings

from .mixins import Six_digit_Gen_Val
from .forms import User_Registration
from .serializer import UserDataSerializer

#This CBV (class based view ) will action as receiving  data from the frontend, will make sure to load the template for the working form
class AsyncRegisterView(View):
    template = 'register.html'
    verification_code = Six_digit_Gen_Val().generator()
    
    async def get(self, request, *args, **kwargs):
        form = User_Registration()
        return render(request, self.template, {'form': form})
    
    @method_decorator(sync_to_async)
    def post(self, request, *args, **kwargs):
        form = User_Registration(self.request.POST)
        if form.is_valid():
            serializer = UserDataSerializer(data=self.request.data)
            if serializer.is_valid():
                if serializer.data['password'] != serializer.data['password_confirmation']:
                    return render(request, self.template, {'form': form, 'error': True})
                serializer.save()
                user = User.objects.get(username = serializer.data["username"])
                user.set_password(raw_password=serializer.data["password"])
                user.save()
                
                response = HttpResponse(headers = self.verification_code)
                
        return render(request, self.template, {'form': form})
'''
This class will be making the validation between user email and the bd

Characteristics
    - This class will take the headers that Registration View set
    - The data in these headers will be used for simple validation data, [code (Will be hashed)]
    - if everything it's correct, the class related to User will be set everything on True
'''
class AsyncVerification(View):
    template = 'email_verification.html'
    h = Hashids(salt=settings.hash_field_salt)
    
    def get(self,request, *args, **kwargs):
        form = User_Registration()
        return render(request, self.template, {"form" : form})
    
    @method_decorator(sync_to_async)
    def post(self, request, *args, **kwargs):
        form = User_Registration(request.POST)
        username = self.request.headers["user"]
        user = get_object_or_404(User, username= username)
        
        if form.is_valid():
            code_input = form.cleaned_data["code"]
            code = self.h.decode(int(self.request.headers["six_digits_code"]))
            
            if code_input != code:
                return render(request, self.template, {"form" : form, "error" : True})
            if str(datetime.now().strftime("%d,%m,%H,%M")) >= self.request.headers["exp_time"]:
                return render(request, self.template, {"form" : form, "error" : True})
            
            user_email_camp = get_object_or_404(UserVerification, user = user.pk)
            user_email_camp.email_verification = True
            user_email_camp.asave()
            
            login(request=self.request, user=user)
            redirect("home")
class AsyncLoginView(View):
    template = 'login.html'
