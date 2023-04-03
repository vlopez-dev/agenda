import factory
from django.contrib.auth.models import User
import pytz

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    is_superuser = False
    is_staff = False
    is_active = True
    date_joined = factory.Faker('date_time_this_century', tzinfo=pytz.UTC)
