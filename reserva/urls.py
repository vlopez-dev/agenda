from django.urls import path,include

from . import views




urlpatterns = [
    path("addreserva/",views.add_reserva,name='add_reserva'),
    path('<int:id>/',views.delete_reserva,name='delete_reserva'),

]
