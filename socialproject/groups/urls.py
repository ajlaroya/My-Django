from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'groups'

urlpatterns = [
    path('',views.ListGroups.as_view(),name='all'),
    path('new/',views.CreateGroup.as_view(),name='create'),
    re_path(r'posts/in/(?P<slug>[-\w]+)/$',views.SingleGroup.as_view(),name='single'),
    re_path(r'join/(?P<slug>[-\w]+)/$',views.JoinGroup.as_view(),name='join'),
    re_path(r'leave/(?P<slug>[-\w]+)/$',views.LeaveGroup.as_view(),name='leave'),
    re_path(r'edit/(?P<slug>[-\w]+)/', views.EditGroup.as_view(), name='edit'),
    re_path(r'delete/(?P<slug>[-\w]+)/',views.DeleteGroup.as_view(),name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
