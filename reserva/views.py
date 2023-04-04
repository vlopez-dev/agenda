from collections import UserList
from datetime import datetime
import threading
from django.shortcuts import redirect, render
from reserva.forms import ReservaForm
import threading

from reserva.models import Reserva
from sala.models import Sala
import sweetify
import pytz
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User
from django.core.mail import send_mail
from agenda.settings import EMAIL_HOST,EMAIL_HOST_PASSWORD,EMAIL_HOST_USER,EMAIL_PORT
from django.core.mail import EmailMessage
from django.core.paginator import Paginator


# Create your views here.
Connected = False


def add_reserva(request, id=0):

    if request.method == "GET":
        if id == 0:
            form = ReservaForm()
        else:
            reserva = Reserva.objects.get(pk=id)

            form = ReservaForm(instance=reserva)
        return render(request, "reserva/add_reserva.html", {"form": form})
    else:
        if id == 0:
            form = ReservaForm(request.POST)
        else:
            reserva = Reserva.objects.get(pk=id)
            form = ReservaForm(request.POST, instance=reserva)
            iniciohora = request.POST.get("tiempo_inicio")

        if form.is_valid():
            salaid = request.POST.get("sala_id")
            iniciohora = request.POST.get("tiempo_inicio")
            dateiniciohora = datetime.strptime(iniciohora, "%d/%m/%Y %H:%M:%S")
            finhora = request.POST.get("tiempo_fin")
            datefinhora = datetime.strptime(finhora, "%d/%m/%Y %H:%M:%S")
            estadosala = verificar_estado(salaid, dateiniciohora, datefinhora)
            invitados = request.POST.get("invitados")
            descripcion = request.POST.get("descripcion")
            if estadosala == False:
                sweetify.error(request, "Sala ocupada", persistent=":(")
            else:

                reserva = form.save(commit=False)
                reserva.username = request.user
                reserva.save()
                send_email(invitados,descripcion,salaid,iniciohora,finhora)
                sweetify.success(
                    request, "Exito", text="Apagado Correctamente", persistent="Aceptar"
                )

        return redirect("/home/")





def send_email(invitados,salaid,descripcion,iniciohora,finhora):
    sender_email= 'agenda@vic.uy'
    recipient_list = invitados.split(";")

    
    email = EmailMessage(
                subject='Correo desde Web',
                body=f'Se realizo una reserva de la sala ' + salaid  + 'para el evento ' + descripcion + ' a la hora de inico ' + iniciohora + ' y finalizacion ' + finhora,
                from_email=sender_email,
                to=recipient_list,
            )
    email.send()





def verificar_estado(salaid, dateiniciohora, datefinhora):
    utc = pytz.UTC
    reservas = Reserva.objects.filter(
        tiempo_fin__range=[dateiniciohora, datefinhora], sala_id_id=salaid
    )
    if not reservas:
        return True
    else:
        return False


def listar_reservas(request):
    
    
    reservas = Reserva.objects.select_related('sala_id','username')
    
    paginator = Paginator(reservas, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    
    context = {
        'page_object': page_object,
    }
    
    return render(request, "reserva/edit_reserva.html", context)









def delete_reserva(request, id_reserva):
    """Eliminacion de una Reserva

    Args:
        request (_type_): _description_
        id_reserva (_type_): Recibo como argumento el id de reserva para
        realizar la busqueda de la misma para su eliminacion

    Returns:
        _type_: Retorno un mensaje con el exito de eliminación
    """
    reserva = Reserva.objects.get(pk=id_reserva)
    reserva.delete()
    sweetify.success(
        request, "Exito", text="Eliminado Correctamente", persistent="Aceptar"
    )

    return redirect("listar_reservas")








def envio_recordatorio(id_reserva):




    subtwo = threading.Thread(target=envio_recordatorio)
    subtwo.start()
