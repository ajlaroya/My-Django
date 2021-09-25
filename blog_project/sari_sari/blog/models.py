from django.db import models
from django.utils import timezone
from django.urls import reverse # after action redirection

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE) # authorised user
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True,null=True)

    # linked to a publish button
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self): # django method to create URL for instance of post
        return reverse('post_detail',kwargs={'pk':self.pk}) # goes poes_detail view with primary key

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE) # comment connected to post
    author = models.CharField(max_length=100)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    # once poster is done with comment, redirects to list of all posts
    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text
