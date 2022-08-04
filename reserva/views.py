from django.shortcuts import redirect, render
from reserva.forms import ReservaForm

from reserva.models import Reserva

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
                    form.save()
                    # sweetify.success(request, 'Exito', text='Agregado Correctamente', persistent='Aceptar')


            return redirect('/home/')



def delete_reserva(request,id):
    reserva = Reserva.objects.get(pk=id)
    reserva.delete()
    # sweetify.success(request, 'Exito', text='Eliminado Correctamente', persistent='Aceptar')

    return redirect('/home')
