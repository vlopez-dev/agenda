from django.shortcuts import render,redirect
from .models import Sala
from reserva.models import Reserva
from .forms import SalaForm
import sweetify

# Create your views here.

def home(request):
    reservas = Reserva.objects.all()
    return render(request,"sala/index.html",{'reservas':reservas})




def add_sala(request,id=0):
    
    if request.method == "GET":
            if id == 0 :
                form = SalaForm()
            else:
                sala = Sala.objects.get(pk=id)

                form = SalaForm(instance=sala)
            return render(request, 'sala/add_sala.html', {'form': form})
    else:
            if id == 0:
                form = SalaForm(request.POST)
            else:
                sala = Sala.objects.get(pk=id)
                form = SalaForm(request.POST,instance= sala)
            if form.is_valid():
                    
                    
                    form.save()
                        
                    sweetify.success(request, 'Exito', text='Apagado Correctamente', persistent='Aceptar')
            


            return redirect('/home/')
        
        
        
        
        

def listar_salas(request):
    context = {'listar_salas': Sala.objects.all()}
    return render(request, "sala/listar_salas.html", context)





def delete_sala(request,id_sala):
    sala = Sala.objects.get(pk=id_sala)
    sala.delete()
    sweetify.success(request, 'Exito', text='Eliminado Correctamente', persistent='Aceptar')

    return redirect('listar_salas')
