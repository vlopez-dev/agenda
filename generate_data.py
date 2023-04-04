import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenda.settings')

import django
django.setup()
from registration.factories import UserFactory
from sala.factories import SalaFactory
from reserva.factories import ReservaFactory

# Genera 10 instancias de modelo
for i in range(1):
    UserFactory()
    

for i in range(25):
     SalaFactory()
    
    
for i in range(25):
    ReservaFactory()