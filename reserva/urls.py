from django.urls import path,include

from . import views




urlpatterns = [
    path("addreserva/",views.add_reserva,name='add_reserva'),
    path('listarreservas/',views.listar_reservas,name='listar_reservas'),
    path('<int:id>/', views.add_reserva,name='reserva_update'),
    path ('<int:id_reserva>/delete_reserva',views.delete_reserva,name='delete_reserva'),



]
