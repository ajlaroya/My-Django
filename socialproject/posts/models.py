from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from groups.models import Group

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    group = models.ForeignKey(Group,related_name='posts',null=True,blank=True,
        on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    image = models.ManyToManyField('Image', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True,
        null=True, related_name='+')
    shared_body = models.TextField(blank=True, null=True)
    shared_on = models.DateTimeField(blank=True, null=True)
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
        blank=True, related_name='+')

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def __str__(self):
        return self.message

    def get_absolute_url(self):
        return reverse('posts:single',kwargs={'username':self.author,'pk':self.pk})

    class Meta:
        ordering = ['-created_at','-shared_on']

class Comment(models.Model):
    comment = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    parent = models.ForeignKey('Comment', on_delete=models.CASCADE, blank=True,
        null=True, related_name='+')

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-timestamp').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)

    def __str__(self):
        return self.image
