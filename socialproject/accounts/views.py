from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.db.models import Q
from posts.models import Post
from .models import UserProfile

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
