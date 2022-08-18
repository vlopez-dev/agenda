from django.urls import path,include
# from rest_framework import routers

from . import views





urlpatterns = [
    path("home/",views.home,name='home'),
    path("addsala/",views.add_sala,name='add_sala'),


]