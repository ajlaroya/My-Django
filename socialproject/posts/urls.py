from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'posts'

urlpatterns = [
    path('',views.PostList.as_view(),name='all'),
    path('new/',views.CreatePost.as_view(),name='create'),
    path('by/<str:username>',views.UserPosts.as_view(),name='for_user'),
    path('by/<str:username>/<int:pk>/',views.PostDetail.as_view(),name='single'),
    path('delete/<int:pk>/',views.DeletePost.as_view(),name='delete'),
    path('edit/<int:pk>/', views.EditPost.as_view(), name='edit'),
    path('like/<int:pk>/', views.AddLike.as_view(), name='like'),
    path('<int:post_pk>/comment/reply/<int:pk>/', views.CommentReplyView.as_view(), name='comment-reply'),
    path('<int:post_pk>/comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
