from django.contrib import admin
from .models import User, UserProfile, Notification, MessageModel

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Notification)
admin.site.register(MessageModel)
