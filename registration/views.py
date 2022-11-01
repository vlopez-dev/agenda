from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserCreationFormWithEmail

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
<<<<<<< HEAD
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    def get_success_url(self):
        return reverse_lazy('login') + '?register'
    
    
    
class PasswordResetView(CreateView):
    form_class = UserCreationFormWithEmail
    success_url = reverse_lazy('login')
    template_name = 'registration/reset-pass.html'
=======
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


    def get_success_url(self) :
        return reverse_lazy('login')+ '?register'

class PasswordResetView(CreateView):
    form_class = UserCreationFormWithEmail
    success_url = reverse_lazy("login")
    template_name = "registration/forgot-password.html"
>>>>>>> main
