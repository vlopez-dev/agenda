from .models import Reserva

def list_notificaciones(request):
    # Fetch last 5 reservations
    recent_reservations = Reserva.objects.all().order_by('-id')[:5]
    return {
        'recent_reservations': recent_reservations,
        'notif_count': recent_reservations.count()
    }
