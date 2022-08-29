from pathlib import Path
from django.urls import path,include
from .views import SignUpView,PasswordResetView




urlpatterns = [
   path('signup/', SignUpView.as_view(), name='signup'),
   path('password_reset/', PasswordResetView.as_view(), name='password_reset'),



]
