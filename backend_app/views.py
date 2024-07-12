from datetime import datetime
import random

from django.core import mail
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views import View
from django.db.utils import IntegrityError
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from asgiref.sync import sync_to_async

from .models import UserVerification
from .forms import User_Registration

#This CBV (class based view ) will action as receiving  data from the frontend, will make sure to load the template for the working form
class AsyncRegisterView(View):
    url_redirect = reverse_lazy("login")
    template = 'register.html'
    
    @method_decorator(sync_to_async)
    def get(self, request, *args, **kwargs):
        form = User_Registration()
        return render(request, self.template, {'form': form})
    
    @method_decorator(sync_to_async)
    def post(self, request, *args, **kwargs):
        form = User_Registration(self.request.POST)
        if form.is_valid():
            
            #This will prevent the 404 error when we call out one user that had been commited into the db
            try:
                if form.cleaned_data['password'] != form.cleaned_data["password_confirmation"]:
                    return render(request, self.template, {'form': form, 'error_1': True})
                user = User(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                )
                user.set_password(form.cleaned_data['password'])
                user.save()
                
                email = UserVerification(
                    user=user
                )
                
                email.save()
                return HttpResponseRedirect(self.url_redirect)
            except IntegrityError as ie:
                return render(request, self.template, {'form': form, 'error_2': True,
                                                       "user": form.cleaned_data["username"]
                                                       })
        return render(request, self.template, {'form': form})

class AsyncLoginView(View):
    template = 'login.html'
    url_redirect = reverse_lazy("home")
    
    @method_decorator(sync_to_async)
    def get(self, request, *args, **kwargs):
        return render(request, self.template)
    
    @method_decorator(sync_to_async)
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username = self.request.POST.get("username"))
        if user.check_password(self.request.POST.get("password")):
            login(self.request, user)
            self.request.session.set_expiry(600)
            return HttpResponseRedirect(self.url_redirect)
        return render(request,self.template, {"error_1" : True} )



'''
This class will be making the validation between user email and the bd

Characteristics
    - This class will take the headers that Registration View set
    - The data in these headers will be used for simple validation data, [code (Will be hashed)]
    - if everything it's correct, the class related to User will be set everything on True
'''

class AsyncAccountSettings(View):
    template = 'accountSettings.html'
    six_digits_code = random.randint(100000, 999999)
    code_verified = False
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username = self.request.user.username)
        email = get_object_or_404(UserVerification, user_id = self.request.user.id)
        code = self.six_digits_code
        
        if email.email_verification == False:
            
            try:
                mail.send_mail(
                subject='Verification code',
                message=f'Your verification code is {code}',
                from_email="no-reply@userVerification.com",
                recipient_list= [user.email],
                fail_silently=False
                )
                
                self.request.session["code_value"] = code
                print(self.request.session["code_value"])
                
            except Exception as e:
                return render(request, self.template, {'error_email': True, 'message': str(e)})

            return render(request, self.template, {"user" : user.username,
                                                   "message_completed": "Verification code has been send to the email direction",
                                                   "verification": False
                                                   })
            
        return render(request, self.template, {"user" : user.username,
                                                "message_verificated": "Your account it's verificated",
                                                "verification": True
                                                })
        
    def post(self, request, *args, **kwargs):
        if 'form_verification' in self.request.POST:
            return self.form_verification(request)
    
    def form_verification(self, request, *args, **kwargs):
        user_input = self.request.POST.get("code")
        print(self.request.session["code_value"])
        if int(user_input) == self.request.session["code_value"]:
            user_id = self.request.user.id
            user_email = get_object_or_404(UserVerification, user = user_id)
            user_email.email_verification = True
            user_email.save()
            return render(request, self.template, {"message_confirmation" : "Verification completed",
                                                   })
        return render(request, self.template, {"error_verification" : True})
            