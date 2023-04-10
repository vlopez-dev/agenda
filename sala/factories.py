import factory
from .models import Sala

class SalaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sala

    nombre = factory.Faker('name')
    ubicacion = factory.Faker('city')
