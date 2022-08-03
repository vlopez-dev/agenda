from pathlib import Path
from django.urls import path,include
from rest_framework import routers
from .views import SignUpView




urlpatterns = [
   path('signup/', SignUpView.as_view(), name='signup')


]
