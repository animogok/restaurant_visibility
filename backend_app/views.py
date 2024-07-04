from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.utils.decorators import method_decorator
from asgiref.sync import sync_to_async

from .mixins import create_or_get_RRG
from .forms import User_Registration

#This CBV (class based view ) will action as receiving  data from the frontend, will make sure to load the template for the working form
class AsyncRegisterView(View):
    template = 'register.html'
    
    async def get(self, request, *args, **kwargs):
        form = User_Registration()
        return render(request, self.template, {'form': form})
    
    @method_decorator(sync_to_async)
    def post(self, request, *args, **kwargs):
        form = User_Registration(self.request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] != form.cleaned_data['password2']:
                return render(request, self.template, {'form': form, 'error': True})
            raw_password = form.cleaned_data["password1"]
            user = User.objects.create(username=form.cleaned_data["username"], first_name=form.cleaned_data["first_name"], 
                                       last_name=form.cleaned_data["last_name"],
                                       email = form.cleaned_data["email"],
                                       password = User.set_password(raw_password=raw_password),
                                       is_active = False
                                       )
            user.asave()
            #Generar un redirect a la pagina de login.
            #El status code predeterminado es el 302
        return render(request, self.template, {'form': form})

class AsyncLoginView(View):
    template = 'login.html'
