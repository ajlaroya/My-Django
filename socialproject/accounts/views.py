''' Views for accounts '''
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from django.http import HttpResponse
from posts.models import Post
from .models import UserProfile, Notification, ThreadModel, MessageModel
from .forms import ThreadForm, MessageForm, ProfileEditForm

class ProfileView(View):
    ''' View for profiles '''
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
    ''' View for editing profiles '''
    model = UserProfile
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('accounts:profile', kwargs={'pk': pk})

class AddFollower(LoginRequiredMixin, View):
    ''' View for following a user '''
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
        notification = Notification.objects.create(notification_type=3,
            from_user=request.user, to_user=profile.user)

        return redirect('accounts:profile', pk=profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
    ''' View for unfollowing a user '''
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('accounts:profile', pk=profile.pk)

class UserSearch(View):
    ''' View for searching user profiles '''
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        if query is None:
            return render(request, 'accounts/search.html')

        else:
            profile_list = UserProfile.objects.filter(
                Q(user__username__icontains=query)
            )
            context = {
                'profile_list': profile_list,
                'query': query,
            }
            return render(request, 'accounts/search.html',context)

class ListFollowers(View):
    ''' View for listing a users followers '''
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()
        context = {
            'profile': profile,
            'followers': followers,
        }
        return render(request, 'accounts/followers_list.html', context)

class PostNotification(View):
    ''' View for post notifications '''
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=object_pk)
        notification.user_has_seen = True
        notification.save()
        return redirect('posts:single', pk=object_pk, username=post.author)

class FollowNotification(View):
    ''' View for follow notifications '''
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = UserProfile.objects.get(pk=object_pk)
        notification.user_has_seen = True
        notification.save()
        return redirect('accounts:profile', pk=object_pk)

class ThreadNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=object_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('accounts:thread', pk=object_pk)

class RemoveNotification(View):
    ''' View for removing notifications '''
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        notification.user_has_seen = True
        notification.save()
        return HttpResponse('Success', content_type='text/plain')

class CreateThread(View):
    ''' View for creating threads '''
    def get(self, request, *args, **kwargs):
        ''' Displays the form to enter a username '''
        form = ThreadForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        ''' Handles creation of thread by grabbing form and see if user matches
        that username. If there is a user, it will check to see if a thread
        exists between the two users already, if there is it will open that
        thread up. If no thread, it will create and redirect to thread. '''
        form = ThreadForm(request.POST)
        username = request.POST.get('username')
        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('accounts:thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('accounts:thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()
                return redirect('accounts:thread', pk=thread.pk)
        except:
            messages.error(request, 'Sorry! cannot find user 😓')
            return redirect('accounts:create-thread')

class ListThreads(View):
    ''' View which acts as a inbox to see all conversations '''
    def get(self, request, *args, **kwargs):
        ''' Grabs all threads where the logged in user is either the sending
        user or receiving user '''
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        context = {
            'threads': threads
        }
        return render(request, 'accounts/inbox.html', context)

class CreateMessage(View):
    ''' View to create message then redirect back to ThreadView '''
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()

        notification = Notification.objects.create(
            notification_type=4,
            from_user=request.user,
            to_user=receiver,
            thread=thread
        )

        return redirect('accounts:thread', pk=pk)

class ThreadView(View):
    ''' View to show all messages in a thread and displays a form at the
    bottom to send a new message '''
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
              'thread': thread,
              'form': form,
              'message_list': message_list
        }
        return render(request, 'accounts/thread.html', context)
