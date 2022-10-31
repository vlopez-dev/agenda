from django.urls import path, include

# from rest_framework import routers

from . import views


urlpatterns = [
    path("home/", views.home, name="home"),
    path("addsala/", views.add_sala, name="add_sala"),
    path("listarsalas/", views.listar_salas, name="listar_salas"),
    path("<int:id_sala>/delete_sala", views.delete_sala, name="delete_sala"),
]
