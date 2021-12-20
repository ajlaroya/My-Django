from django.contrib import admin
from .models import User, UserProfile, Notification, MessageModel, Contact

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Notification)
admin.site.register(MessageModel)
admin.site.register(Contact)
