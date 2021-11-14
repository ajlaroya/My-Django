from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from posts.models import Post
from .models import User,UserProfile
from . import forms

# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(user=user).order_by('-created_at')
        followers = profile.followers.all()
        is_following = False

        for follower in followers:
            if follower == user:
                is_following = True
                break
            else:
                is_following = False

        follower_count = len(followers)

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'is_following': is_following,
            'follower_count': follower_count,
            'followers': followers,
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
        my_user = User.objects.get(pk=pk)
        profile.followers.add(my_user)
        return redirect('accounts:profile', pk=profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        my_user = User.objects.get(pk=pk)
        profile.followers.remove(my_user)
        return redirect('accounts:profile', pk=profile.pk)
