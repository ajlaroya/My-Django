from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class UserProfile(models.Model):
    ''' Model for user profiles '''
    user = models.OneToOneField(User, primary_key=True, verbose_name='user',
        related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures/',
        default='uploads/profile_pictures/default.png', blank=True)
    followers = models.ManyToManyField(User, blank=True,
        related_name='followers')

    def __str__(self):
        return f"{self.user} profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    ''' Creates user profile instance on registration '''
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        UserProfile.objects.create(user=instance)

class Notification(models.Model):
    ''' Model for notifications, notification types:
    1 = Like, 2 = Comment, 3 = Follow, 4 = DMs '''
    notification_type = models.IntegerField(null=True, blank=True)
    to_user = models.ForeignKey(User, related_name='notification_to',
        on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from',
        on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE,
        related_name='+', blank=True, null=True)
    comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE,
        related_name='+', blank=True, null=True)
    thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE,
        related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)

# Sending and receiving direct messages
class ThreadModel(models.Model):
    ''' Model for all messages between two users '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    has_unread = models.BooleanField(default=False)

class MessageModel(models.Model):
    ''' Model for individual message '''
    thread = models.ForeignKey('ThreadModel', related_name='+',
        on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='uploads/message_photos', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.body

# Contact page
class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email
