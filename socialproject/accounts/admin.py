from django.contrib import admin
from .models import User, UserProfile, Notification

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Notification)
