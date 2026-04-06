import os
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenda.settings')
django.setup()

from registration.factories import UserFactory
from sala.factories import SalaFactory
from reserva.factories import ReservaFactory

# Genera 10 Salas con colores variados
salas = [SalaFactory() for _ in range(10)]

# Genera 5 Usuarios
users = [UserFactory() for _ in range(5)]

# Genera 50 Reservas distribuidas entre las salas y usuarios creados
# Las duraciones son cortas (1 hora) por defecto en ReservaFactory
for _ in range(50):
    ReservaFactory(
        sala_id=random.choice(salas),
        username=random.choice(users)
    )

print("Datos generados correctamente: 10 salas, 5 usuarios y 50 reservas.")