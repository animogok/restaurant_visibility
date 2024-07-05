from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.utils.decorators import method_decorator
from asgiref.sync import sync_to_async

from .mixins import create_or_get_RRG
from .forms import User_Registration
from .serializer import UserDataSerializer

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
            serializer = UserDataSerializer(data=self.request.data)
            if serializer.is_valid():
                if serializer.data['password'] != serializer.data['password_confirmation']:
                    return render(request, self.template, {'form': form, 'error': True})
                serializer.save()
                user = User.objects.get(username = serializer.data["username"])
                user.set_password(raw_password=serializer.data["password"])
                user.save()
                
                #Generar la redireccion, ademas buscar la informacion referente a si los datos "no verificados" se deben de eliminar o dejar ahi
                #En caso de eliminar, generar en esta clase las formas correspondientes para poder hacer eso.
                
                #Ver si se puede agrear el id_user al header en la redireccion por el 302, en caso de que se pueda, extraer ese header y aplicar con la verificacion
                
                #En caso de que no se pueda, generar la serializacion por token y ponerlo en el header, y generar el mismo procedimiento.
                
        return render(request, self.template, {'form': form})

class AsyncVerification(View):
    template = 'email_verification.html'
   
    
    def get(self,request, *args, **kwargs):
        form = '' #agregar formulario en forms.py
        return render(request, self.template, {"form" : form})
    
    @method_decorator(sync_to_async)
    def post(self, request, *args, **kwargs):
        form = '' #agregar formulario en forms.py
        user_id = "" #Extraer el header
        
        if form.is_valid():
            #Verificar si el usuario existe, en caso de que no, generar un error y red
            pass
        
class AsyncLoginView(View):
    template = 'login.html'
