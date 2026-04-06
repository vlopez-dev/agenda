import factory
import pytz
import random
from datetime import timedelta, datetime
from .models import Reserva
from sala.factories import SalaFactory
from registration.factories import UserFactory

def get_random_time_outside_office_hours():
    # Target hours: 0-8 or 18-23
    if random.choice([True, False]):
        hour = random.randint(0, 8)
    else:
        hour = random.randint(18, 23)
    
    # Random day this month
    now = datetime.now()
    day = random.randint(1, 28)
    return datetime(now.year, now.month, day, hour, random.randint(0, 59), tzinfo=pytz.UTC)

class ReservaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reserva

    titulo = factory.Faker('sentence', nb_words=3)
    tiempo_inicio = factory.LazyFunction(get_random_time_outside_office_hours)
    tiempo_fin = factory.LazyAttribute(lambda o: o.tiempo_inicio + timedelta(hours=1))
    username = factory.SubFactory(UserFactory)
    descripcion = factory.Faker('text', max_nb_chars=500)
    sala_id = factory.SubFactory(SalaFactory)
    invitados = factory.Faker('name')
    recordatorio = factory.Faker('boolean')
