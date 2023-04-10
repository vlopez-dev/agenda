from django.urls import path, include

from . import views


urlpatterns = [
    path("addreserva/", views.add_reserva, name="add_reserva"),
    path("listarreservas/", views.listar_reservas, name="listar_reservas"),
    path("<int:id>/", views.add_reserva, name="reserva_update"),
    path("delete_reserva_all/", views.delete_reserva_all, name="delete_reserva_all"
    ),
]
