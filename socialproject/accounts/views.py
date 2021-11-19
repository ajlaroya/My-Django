from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.db.models import Q
from posts.models import Post
from .models import UserProfile, Notification

class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_at')
        followers = profile.followers.all()
        follower_count = len(followers)

        if follower_count == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False


        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'is_following': is_following,
            'follower_count': follower_count,
        }

        return render(request, 'accounts/profile.html', context)

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['bio', 'location', 'picture']
    template_name = 'accounts/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('accounts:profile', kwargs={'pk': pk})

class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
        notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)

        return redirect('accounts:profile', pk=profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('accounts:profile', pk=profile.pk)

class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query)
        )
        context = {
            'profile_list': profile_list,
            'query': query,
        }
        return render(request, 'accounts/search.html', context)

class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()
        context = {
            'profile': profile,
            'followers': followers,
        }
        return render(request, 'accounts/followers_list.html', context)

class PostNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=object_pk)
        notification.user_has_seen = True
        notification.save()
        return redirect('posts:single', pk=object_pk, username=post.author)

class FollowNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = UserProfile.objects.get(pk=object_pk)
        notification.user_has_seen = True
        notification.save()
        return redirect('accounts:profile', pk=object_pk)

class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        notification.user_has_seen = True
        notification.save()
        return HttpResponse('Success', content_type='text/plain')
