from collections import UserList
from datetime import datetime
from django.shortcuts import redirect, render
from reserva.forms import ReservaForm

from reserva.models import Reserva
from sala.models import Sala
import sweetify
import pytz
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User

# Create your views here.

def add_reserva(request,id=0):
    
    if request.method == "GET":
            if id == 0 :
                form = ReservaForm()
            else:
                reserva = Reserva.objects.get(pk=id)

                form = ReservaForm(instance=reserva)
            return render(request, 'reserva/add_reserva.html', {'form': form})
    else:
            if id == 0:
                form = ReservaForm(request.POST)
            else:
                reserva = Reserva.objects.get(pk=id)
                form = ReservaForm(request.POST,instance= reserva)
                iniciohora=request.POST.get('tiempo_inicio')

            if form.is_valid():
                    salaid=request.POST.get('sala_id')
                    iniciohora=request.POST.get('tiempo_inicio')
                    dateiniciohora = datetime.strptime(iniciohora, '%d/%m/%Y %H:%M:%S')
                    finhora=request.POST.get('tiempo_fin')
                    datefinhora = datetime.strptime(finhora,'%d/%m/%Y %H:%M:%S')
                    estadosala=verificar_estado(salaid,dateiniciohora,datefinhora)
                    if estadosala==False:
                        sweetify.error(request, 'Sala ocupada', persistent=':(')
                    else:
                        
                        reserva =form.save(commit=False)
                        reserva.username=request.user
                        reserva.save()
                        sweetify.success(request, 'Exito', text='Apagado Correctamente', persistent='Aceptar')


            return redirect('/home/')



def verificar_estado(salaid,dateiniciohora,datefinhora):
    utc=pytz.UTC
    reservas = Reserva.objects.filter(tiempo_fin__range=[dateiniciohora,datefinhora],sala_id_id=salaid)
    if not reservas:
        return True
    else:
        return False





def listar_reservas(request):
    context = {'listar_reservas': Reserva.objects.all(),'salas':Sala.objects.all(),'users':User.objects.all()}
    return render(request, "reserva/edit_reserva.html", context)








def delete_reserva(request,id_reserva):
    reserva = Reserva.objects.get(pk=id_reserva)
    reserva.delete()
    sweetify.success(request, 'Exito', text='Eliminado Correctamente', persistent='Aceptar')

    return redirect('listar_reservas')



