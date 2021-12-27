from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from accounts.models import UserProfile
from posts.models import Post
from groups.models import Group

class Command(BaseCommand):
    help = "Command information"

    def handle(self,*args,**kwargs):
        fake = Faker()

        # print(fake.user_name())
        # print(fake.free_email())
        # print(fake.password())
        # print(fake.paragraph(nb_sentences=5))

        for _ in range(9):
            # Generating User
            email = fake.unique.free_email()
            username = fake.unique.user_name()
            password = make_password('password')
            User.objects.create(email=email,username=username,password=password)
            userobj = User.objects.get(username=username)

            # Generating Profile
            bio = fake.catch_phrase()
            location = fake.location_on_land()[2]
            # picture = make_password('password')
            profile = UserProfile(user_id=userobj.pk,bio=bio,location=location)
            profile.save()

            # Generating Posts
            message = fake.paragraph(nb_sentences=5)
            Post.objects.create(author=userobj,message=message)

            # Generating Groups
            print(f'{username} created')
            print(message)

        check_users = User.objects.all().count()
        check_posts = Post.objects.all().count()
        self.stdout.write(self.style.SUCCESS(f'Number of users: {check_users}'))
        self.stdout.write(self.style.SUCCESS(f'Number of posts: {check_posts}'))
