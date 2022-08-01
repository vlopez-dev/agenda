from django.shortcuts import render

from reserva.models import Reserva

# Create your views here.

def index(request):
    reservas = Reserva.objects.all()
    return render(request,"sala/index.html",{'reservas':reservas})
