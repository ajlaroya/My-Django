from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Command information"

    def handle(self,*args,**kwargs):
        fake = Faker()

        # print(fake.user_name())
        # print(fake.free_email())
        # print(fake.password())
        # print(fake.paragraph(nb_sentences=5))

        for _ in range(10):
            email = fake.unique.free_email()
            username = fake.unique.user_name()
            password = make_password('password')
            User.objects.create(email=email,username=username,password=password)
            print(f'{username} created')

        check_users = User.objects.all().count()
        self.stdout.write(self.style.SUCCESS(f'Number of users: {check_users}'))
