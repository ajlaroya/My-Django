import io
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.core.files.images import ImageFile
from accounts.models import UserProfile
from posts.models import Post
from groups.models import Group
from convokit import Corpus, download

class Command(BaseCommand):
    help = "Command information"

    def handle(self,*args,**kwargs):
        fake = Faker()
        print('Downloading corpus')
        corpus = Corpus(filename=download("reddit-corpus-small"))

        for _ in range(25):
            utt = corpus.random_utterance()
            text = utt.text

            # Generating User
            email = fake.unique.free_email()
            username = fake.unique.user_name()
            password = make_password('password')
            User.objects.create(email=email,username=username,password=password)
            userobj = User.objects.get(username=username)

            print(f'User: {username} created')

            # Generating Profile
            catch_phrase = fake.catch_phrase()
            bio = f'[hi, im a generated user] {catch_phrase}'
            location = fake.location_on_land()[2] + ', ' + fake.location_on_land()[3]
            # picture = fake.image()
            # avatar = ImageFile(io.BytesIO(picture), name='foo.jpg')
            profile = UserProfile(user_id=userobj.pk,bio=bio,location=location)
            profile.save()

            print(f'Bio: {bio}')
            print(f'Location: {location}')

            # Generating Groups
            subreddit = utt.meta['subreddit']
            try:
                Group.objects.create(name=subreddit)
            except IntegrityError:
                print(f"{subreddit} already exists")

            group = Group.objects.get(name=subreddit)

            print(f'Group: {subreddit} created')

            # Generating Posts
            Post.objects.create(author=userobj,message=text,group=group)

            print(f'Post: {text} \n')


        check_users = User.objects.all().count()
        check_posts = Post.objects.all().count()
        self.stdout.write(self.style.SUCCESS(f'Number of users: {check_users}'))
        self.stdout.write(self.style.SUCCESS(f'Number of posts: {check_posts}'))
