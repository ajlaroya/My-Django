import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ProTwo.settings')

import django
django.setup()

# Fake population JavaScript
import random
from AppTwo.models import User
from faker import Faker

fakegen = Faker()

def populate(N=5):

    for entry in range(N):

        # Create fake data for that entry
        fake_first = fakegen.first_name()
        fake_last = fakegen.last_name()
        fake_email = fakegen.email()

        # Create new user entry
        users = User.objects.get_or_create(first_name=fake_first,last_name=fake_last,email=fake_email)[0]

if __name__ == '__main__':
    print("Populating script!")
    populate(20)
    print("Populating complete!")
