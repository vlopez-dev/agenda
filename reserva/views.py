from collections import UserList
from datetime import datetime
from smtplib import SMTPAuthenticationError
import threading
from django.shortcuts import redirect, render
from reserva.forms import ReservaForm
import threading
from django.contrib.auth.decorators import login_required, permission_required

from reserva.models import Reserva
from sala.models import Sala
import sweetify
import pytz
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User
from django.core.mail import send_mail, get_connection, EmailMessage
from agenda.settings import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT
from django.core.paginator import Paginator
from django.contrib import messages
from configuracion.models import ConfigEmail
import logging
import uuid

logger = logging.getLogger("agenda")


# Create your views here.
Connected = False


@login_required
@permission_required("reserva.add_reserva", raise_exception=True)
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
                print(invitados)
                result_env = send_email(
                    invitados,
                    descripcion,
                    salaid,
                    iniciohora,
                    finhora,
                    asunto="Reserva Realizada",
                )
                if result_env == None:
                    sweetify.error(
                        request,
                        "Error en el envio de mail, se realizo la reserva igualmente",
                        persistent=":(",
                    )

                else:
                    sweetify.success(
                        request,
                        "Exito",
                        text="Apagado Correctamente",
                        persistent="Aceptar",
                    )

        return redirect("/home/")


def generate_ics(titulo, descripcion, sala, inicio, fin):
    """Genera el contenido de un archivo .ics para el calendario"""
    # Formatear fechas para ICS (YYYYMMDDTHHMMSSZ)
    def fmt(dt_str):
        dt = datetime.strptime(dt_str, "%d/%m/%Y %H:%M:%S")
        return dt.strftime("%Y%m%dT%H%M%SZ")

    ics_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Agenda App//ES",
        "METHOD:REQUEST",
        "BEGIN:VEVENT",
        f"UID:{uuid.uuid4()}",
        f"DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}",
        f"DTSTART:{fmt(inicio)}",
        f"DTEND:{fmt(fin)}",
        f"SUMMARY:{titulo}",
        f"DESCRIPTION:{descripcion}",
        f"LOCATION:{sala}",
        "END:VEVENT",
        "END:VCALENDAR"
    ]
    return "\n".join(ics_content)


def send_email(invitados, descripcion, salaid, iniciohora, finhora, asunto):
    config = ConfigEmail.objects.last()
    
    # Configuramos la conexión dinámicamente si existe configuración en DB
    connection = None
    from_email = "web@vic.uy"
    
    if config:
        from_email = config.default_from_email
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=config.email_host,
            port=config.host_port,
            username=config.host_user,
            password=config.host_password,
            use_tls=config.use_tls,
            use_ssl=config.use_ssl,
        )

    recipient_list = invitados.split(";")
    
    body = (
        f"Se realizó una reserva de la sala {salaid} para el evento: {descripcion}\n\n"
        f"Inicio: {iniciohora}\n"
        f"Fin: {finhora}\n\n"
        "Se adjunta la invitación para su calendario."
    )

    email = EmailMessage(
        subject=asunto,
        body=body,
        from_email=from_email,
        to=recipient_list,
        connection=connection
    )

    # Generar y adjuntar archivo ICS
    ics_data = generate_ics(asunto, descripcion, salaid, iniciohora, finhora)
    email.attach("invitacion.ics", ics_data, "text/calendar")

    try:
        logger.debug("Intentando enviar email con invitación de calendario")
        email.send()
        return True
    except Exception as e:
        logger.error(f"Error al enviar email: {str(e)}")
        return None


def verificar_estado(salaid, dateiniciohora, datefinhora):
    utc = pytz.UTC
    reservas = Reserva.objects.filter(
        tiempo_fin__range=[dateiniciohora, datefinhora], sala_id_id=salaid
    )
    if not reservas:
        return True
    else:
        return False


@login_required
@permission_required("reserva.view_reserva", raise_exception=True)
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


@login_required
@permission_required("reserva.delete_reserva", raise_exception=True)
def delete_reserva_all(request):
    if request.method == "POST":
        ids_reserva_delete = request.POST.getlist("ids_reserva_delete")
        ids_reserva_delete = list(map(int, ids_reserva_delete))

        reservas = Reserva.objects.filter(id__in=ids_reserva_delete)
        if ids_reserva_delete != []:
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
                print(cancelacion)
                if cancelacion == True:
                    reserva.delete()
                    sweetify.success(
                        request,
                        "Exito",
                        text="Eliminado Correctamente",
                        persistent="Aceptar",
                    )
                else:
                    sweetify.error(
                        request,
                        "Error",
                        text="No se pudo enviar el correo de cancelación, pero igualmente se elimina del sistema",
                        persistent="Aceptar",
                    )
                    reserva.delete()

            return redirect("listar_reservas")

        else:
            sweetify.error(
                request,
                "Error",
                text="Debe seleccionar al menos una sala",
                persistent="Aceptar",
            )
            return redirect("listar_reservas")

    else:
        reservas = Reserva.objects.all()
        return redirect("listar_reservas", {"reservas": reservas})


@login_required
@permission_required("reserva.change_reserva", raise_exception=True)
def editar_reserva(request, id):
    reserva = Reserva.objects.get(pk=id)
    if request.method == "GET":
        form = ReservaForm(instance=reserva)
        return render(request, "reserva/add_reserva.html", {"form": form})
    else:
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            dateiniciohora = datetime.strftime(reserva.tiempo_inicio, "%d/%m/%Y %H:%M:%S")
            datefinhora = datetime.strftime(reserva.tiempo_fin, "%d/%m/%Y %H:%M:%S")

            modificacion = send_email(
                    invitados=reserva.invitados,
                    descripcion=reserva.descripcion,
                    salaid=reserva.sala_id.nombre,
                    iniciohora=dateiniciohora,
                    finhora=datefinhora,
                    asunto="Reserva Modificada",
                )
            if modificacion == True:
                reserva.save()
           
                sweetify.success(request, "Exito", text="Editado Correctamente", persistent="Aceptar")
            else:
                sweetify.error(request, "Error", text="No se pudo enviar el correo de modificación", persistent="Aceptar")
                reserva.save()
        
        else:
            sweetify.error(request, "Error", text="No se pudo editar", persistent="Aceptar")
        return redirect("/home/")


# def envio_recordatorio(id_reserva):
#     subtwo = threading.Thread(target=envio_recordatorio)
#     subtwo.start()
