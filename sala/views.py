from django.shortcuts import render, redirect, HttpResponse

from .models import Sala
from reserva.models import Reserva
from .forms import SalaForm
import sweetify
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
@login_required
def home(request):
    reservas = Reserva.objects.all()
    salas = Sala.objects.all()
    return render(request, "sala/index.html", {"reservas": reservas, "salas": salas})


@login_required
def add_sala(request, id=0):
    """_summary_
    Funcion para agregar Sala.
    Args:
        request (_type_): _description_
        id (int, optional): Tiene como argumento un id=0 por defecto. Defaults to 0.

    Returns:
        _type_:Se retorna un mensaje  con lieria sweetify.
    """
    if request.method == "GET":
        if id == 0:
            form = SalaForm()
        else:
            sala = Sala.objects.get(pk=id)

            form = SalaForm(instance=sala)
        return render(request, "sala/add_sala.html", {"form": form})
    else:
        if id == 0:
            form = SalaForm(request.POST)
        else:
            sala = Sala.objects.get(pk=id)
            form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            sweetify.success(
                request, "Exito", text="Agregado Correctamente", persistent="Aceptar"
            )
        return redirect("/home/")


@login_required
def listar_salas(request):
    """
    Función para listar todas las Salas

    Args:
        request (_type_): _description_

    Returns:
        _type_: Retorno context con todas salas
    """
    elements = Sala.objects.all()
    paginator = Paginator(elements,10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    context ={
        'page_object':page_object,
    }
    
    return render(request, "sala/listar_salas.html", context)


@login_required
def delete_sala(request, id_sala):
    """Funcion para la eliminación de una sala

    Args:
        request (_type_): _description_
        id_sala (_type_): id correspondiente a la sala

    Returns:
        _type_: Retorno un mensaje de exito cuando es eliminado
    """
    sala = Sala.objects.get(pk=id_sala)
    sala.delete()
    sweetify.success(
        request, "Exito", text="Eliminado Correctamente", persistent="Aceptar"
    )

    return redirect("listar_salas")





def delete_salas_all(request):
    if request.method == 'POST':
        ids_sala_delete = request.POST.getlist('ids_sala_delete')
        ids_sala_delete = list(map(int, ids_sala_delete))

        print(type(ids_sala_delete))
        Sala.objects.filter(id__in=ids_sala_delete).delete()  
        return redirect("listar_salas")
        
    else:
        reservas = Reserva.objects.all()
        return redirect("listar_salas",{'reservas':reservas})

