from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserCreationFormWithEmail
from django.core.mail import send_mail
from django.conf import settings
from agenda.settings import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


    def get_success_url(self) :
        return reverse_lazy('login')+ '?register'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        
        
        # sendemail from new users
        subject = 'Bienvenido a Agenda'
        message = 'Hola {} te damos la bienvenida a Agenda'.format(user.username)
        from_email =EMAIL_HOST_USER
        recipent_list= [user.email]
        send_mail(subject, message, from_email, recipent_list)
        return response

class PasswordResetView(CreateView):
    form_class = UserCreationFormWithEmail
    success_url = reverse_lazy("login")
    template_name = "registration/forgot-password.html"


    def form_valid(self, form):
        response = super().form_valid(form)
        user=form.cleaned_data['email']
        
        subject = 'Olvidaste tu Contraseña'
        message = 'Hola {}, hemos recibido una solicitud para reiniciar tu contraseña. Haz clic en el siguiente enlace para crear una nueva contraseña: {}'.format(user.username, self.get_success_url())
        from_email = EMAIL_HOST_USER
        recipient_list= [user.email]
        send_mail(subject,message,from_email,recipient_list)
        return response