import imp
from django.shortcuts import redirect, render
from reserva.forms import ReservaForm

from reserva.models import Reserva
from sala.models import Sala
import sweetify

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
            if form.is_valid():
                    salaid=request.POST.get('sala_id')
                    estadosala=verificar_estado(salaid)
                    if estadosala==True:
                        sweetify.error(request, 'Sala ocupada', persistent=':(')

                        print("sala ocupada")
                        print(estadosala)
                    else:
                        print("sala libre")
                        print(estadosala)
                        cambiar_estado(salaid)
                        form.save()
                        
                        sweetify.success(request, 'Exito', text='Apagado Correctamente', persistent='Aceptar')


            return redirect('/home/')



def verificar_estado(salaid):
    sala= Sala.objects.get(id=salaid)
    estado=sala.estado
    return estado


def cambiar_estado(salaid):
    Sala.objects.filter(pk=salaid).update(estado=True)





def listar_reservas(request):
    context = {'listar_reservas': Reserva.objects.all()}
    return render(request, "reserva/edit_reserva.html", context)








def delete_reserva(request,id_reserva):
    reserva = Reserva.objects.get(pk=id_reserva)
    salaid=reserva.sala_id_id
    Sala.objects.filter(pk=salaid).update(estado=False)

    reserva.delete()
    sweetify.success(request, 'Exito', text='Eliminado Correctamente', persistent='Aceptar')

    return redirect('home')
