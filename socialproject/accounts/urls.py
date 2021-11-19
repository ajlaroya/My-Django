from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', views.ProfileEditView.as_view(), name='profile-edit'),
    path('profile/<int:pk>/followers/add', views.AddFollower.as_view(), name='add-follower'),
    path('profile/<int:pk>/followers/remove', views.RemoveFollower.as_view(), name='remove-follower'),
    path('profile/<int:pk>/followers', views.ListFollowers.as_view(), name='followers-list'),
    path('search/', views.UserSearch.as_view(), name='profile-search'),
    path('notification/<int:notification_pk>/post/<int:object_pk>', views.PostNotification.as_view(), name='post-notification'),
    path('notification/<int:notification_pk>/follow/<int:object_pk>', views.FollowNotification.as_view(), name='follow-notification'),
    path('notification/delete/<int:notification_pk>', views.RemoveNotification.as_view(), name='notification-delete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
