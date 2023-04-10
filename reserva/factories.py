import factory
import pytz
from .models import Reserva
from sala.factories import SalaFactory
from registration.factories import UserFactory


class ReservaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reserva

    titulo = factory.Faker('sentence', nb_words=4)
    tiempo_inicio = factory.Faker('date_time', tzinfo=pytz.UTC)
    tiempo_fin = factory.Faker('date_time', tzinfo=pytz.UTC)
    username = factory.SubFactory(UserFactory)
    descripcion = factory.Faker('text', max_nb_chars=500)
    sala_id = factory.SubFactory(SalaFactory)
    invitados = factory.Faker('name')
    recordatorio = factory.Faker('boolean')
