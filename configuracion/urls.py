from django.urls import path,include

from . import views




urlpatterns = [
    path("addconfigemail/",views.add_confemail,name='add_configemail'),
   



]
