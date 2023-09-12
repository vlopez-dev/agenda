from collections import UserList
from datetime import datetime
from smtplib import SMTPAuthenticationError
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
from agenda.settings import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.contrib import messages
import logging

logger = logging.getLogger("agenda")


# Create your views here.
Connected = False


def add_reserva(request,id=0):
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
                result_env = send_email(
                    invitados,
                    descripcion,
                    salaid,
                    iniciohora,
                    finhora,
                    asunto="Reserva",
                )
                if result_env == None:
                    sweetify.error(request, 'Error en el envio de mail, se realizo la reserva igualmente', persistent=":(")

                else:
                    sweetify.success(
                        request,
                        "Exito",
                        text="Apagado Correctamente",
                        persistent="Aceptar",
                    )

        return redirect("/home/")


def send_email(invitados, descripcion, salaid, iniciohora, finhora, asunto):
    sender_email = "web@vic.uy"
    recipient_list = invitados.split(";")
    logger.debug(EMAIL_HOST_USER)

    email = EmailMessage(
        subject=asunto,
        body=f"Se realizo una reserva de la sala "
        + salaid
        + "para el evento "
        + descripcion
        + " a la hora de inico "
        + iniciohora
        + " y finalizacion "
        + finhora,
        from_email=sender_email,
        to=recipient_list,
    )
    try:
        logger.debug("Entre al try para enviar el email")

        email.send()
        return True

    except SMTPAuthenticationError as auth_error:
        logger.error(f"Error de autenticación SMTP: {str(auth_error)}")
        return None

    except Exception as e:
        logger.error(f"Otro error: {str(e)}")
        return None

    finally:
        email.get_connection().close()


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
    reservas = Reserva.objects.select_related("sala_id", "username").order_by(
        "tiempo_inicio"
    )

    paginator = Paginator(reservas, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    context = {
        "page_object": page_object,
    }

    return render(request, "reserva/edit_reserva.html", context)


def delete_reserva_all(request):
    if request.method == "POST":
        ids_reserva_delete = request.POST.getlist("ids_reserva_delete")
        ids_reserva_delete = list(map(int, ids_reserva_delete))

        reservas = Reserva.objects.filter(id__in=ids_reserva_delete)
        for reserva in reservas:
            dateiniciohora = datetime.strftime(
                reserva.tiempo_inicio, "%d/%m/%Y %H:%M:%S"
            )
            datefinhora = datetime.strftime(reserva.tiempo_fin, "%d/%m/%Y %H:%M:%S")

            cancelacion = send_email(
                invitados=reserva.invitados,
                descripcion=reserva.descripcion,
                salaid=reserva.sala_id.nombre,
                iniciohora=dateiniciohora,
                finhora=datefinhora,
                asunto="Reserva Cancelada",
            )

            if cancelacion == True:
                sweetify.success(
                    request,
                    "Exito",
                    text="Eliminado Correctamente",
                    persistent="Aceptar",
                )
                reserva.delete()
            else:
         
                sweetify.error(request, "Error", text="No se pudo enviar el correo de cancelación, pero igualmente se elimina del sistema", persistent="Aceptar")   
                reserva.delete()

        return redirect("listar_reservas")
    else:
        reservas = Reserva.objects.all()
        return redirect("listar_reservas", {"reservas": reservas})


def envio_recordatorio(id_reserva):
    subtwo = threading.Thread(target=envio_recordatorio)
    subtwo.start()
