from django.contrib import admin
from .models import User, UserProfile, Notification, MessageModel, Contact
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Notification)
admin.site.register(MessageModel)
admin.site.register(Contact)

class MyUserAdmin(UserAdmin):
    # override the default sort column
    ordering = ('date_joined', )
    # if you want the date they joined or other columns displayed in the list,
    # override list_display too
    list_display = ('username', 'email', 'date_joined', 'first_name', 'last_name', 'is_staff')

# finally replace the default UserAdmin with yours
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
