from django.urls import re_path
from basicforms import views

urlpatterns = [
    re_path(r'^$',views.form_view,name='forms'),
]
