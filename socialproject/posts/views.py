from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404, HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth.models import User

from braces.views import SelectRelatedMixin

from accounts.models import Notification
from .models import Post, Comment, Image, Tag
from .forms import PostForm, CommentForm, ShareForm, ExploreForm

# Create your views here.
class PostList(LoginRequiredMixin,generic.View):
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user

        # shows only posts from users that are followed
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        )
        form = PostForm()
        share_form = ShareForm()
        reply_form = CommentForm()

        context = {
            'post_list': posts,
            'form': form,
            'shareform': share_form,
            'reply_form':reply_form
        }

        return render(request, 'posts/post_list.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_at')
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        share_form = ShareForm()

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            new_post.create_tags()

            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()

        context = {
            'post_list': posts,
            'form': form,
            'shareform': share_form,
        }

        return render(request, 'posts/post_list.html', context)

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        share_form = ShareForm()
        reply_form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-timestamp')
        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'shareform':share_form,
            'reply_form':reply_form
        }
        return render(request, 'posts/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        # form = PostForm(request.POST, request.FILES)
        form = CommentForm(request.POST)
        share_form = ShareForm()

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            new_comment.create_tags()

        comments = Comment.objects.filter(post=post).order_by('-timestamp')

        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)

        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'shareform':share_form,
        }
        return render(request, 'posts/post_detail.html', context)

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    model = Post
    fields = ('message','group','image')

    def get(self, request, *args, **kwargs):
        form = PostForm()

        context = {
            'form': form,
        }

        return render(request, 'posts/post_form.html', context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            new_post.create_tags()

            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()

        context = {
            'form': form,
        }

        return redirect('posts:all')

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = Post
    select_related = ('author','group')
    success_url = reverse_lazy('posts:all')

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(author_id = self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)

class EditPost(LoginRequiredMixin,SelectRelatedMixin,generic.UpdateView):
    model = Post
    select_related = ('author',)
    template_name = 'posts/post_edit.html'
    form_class = PostForm

    def post(self, request, pk, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')

        if form.is_valid():
            post = Post.objects.get(pk=pk)
            form = PostForm(request.POST, instance=post)
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            new_post.create_tags()

            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()

        context = {
            'form': form,
        }

        return redirect('posts:all')

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('posts:single', kwargs={'pk': pk, 'username':self.request.user})

class AddLike(LoginRequiredMixin, generic.View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post)


        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class PostReplyView(LoginRequiredMixin, generic.View):
    def post(self, request, post_pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            new_comment.create_tags()

        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, comment=new_comment)

        return redirect('posts:single', username=post.author, pk=post_pk)

class CommentReplyView(LoginRequiredMixin, generic.View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

            new_comment.create_tags()

        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=parent_comment.author, comment=new_comment)

        return redirect('posts:single', username=post.author, pk=post_pk)

class CommentDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Comment
    template_name = 'posts/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('posts:single', kwargs={'pk': pk, 'username':self.request.user})

class AddCommentLike(LoginRequiredMixin, generic.View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        is_like = False
        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            comment.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=comment.author, comment=comment)

        if is_like:
            comment.likes.remove(request.user)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class SharedPostView(generic.View):
    ''' View to handle post request when sharing a post,
    creates a new post with all the data and redirects back to post list'''
    def post(self, request, pk, *args, **kwargs):
        original_post = Post.objects.get(pk=pk)
        form = ShareForm(request.POST)

        if form.is_valid():
            new_post = Post(
                shared_body = self.request.POST.get('body'),
                message = original_post.message,
                author = original_post.author,
                created_at = original_post.created_at,
                shared_on = timezone.now(),
                shared_user = request.user
            )

            new_post.save()

            for img in original_post.image.all():
                new_post.image.add(img)

            new_post.save()

        return redirect('posts:all')

class Explore(generic.View):
    ''' Looks for query and returns tag with that name and filters posts'''
    def get(self, request, *args, **kwargs):
        explore_form = ExploreForm()
        share_form = ShareForm()
        reply_form = CommentForm()
        query = self.request.GET.get('query')
        tag = Tag.objects.filter(name=query).first()

        if tag:
            # filter posts by tag
            posts = Post.objects.filter(tags__in=[tag])
        else:
            # show all posts
            posts = Post.objects.all()

        context = {
          'tag': tag,
          'posts': posts,
          'explore_form': explore_form,
          'shareform':share_form,
          'reply_form':reply_form
        }

        return render(request, 'posts/explore.html', context)

    def post(self, request, *args, **kwargs):
        ''' HttpResponseRedirect allows us to pass in a URL string which
        we can add the query at the end of it.'''
        explore_form = ExploreForm(request.POST)
        if explore_form.is_valid():
            query = explore_form.cleaned_data['query']
            tag = Tag.objects.filter(name=query).first()

            posts = None
            if tag:
                # filter posts by tag
                posts = Post.objects.filter(tags__in=[tag])

            if posts:
                context = {
                    'tag': tag,
                    'posts': posts,
                }
            else:
                context = {
                    'tag': tag
                }
            return HttpResponseRedirect(f'/posts/explore?query={query}')
        return HttpResponseRedirect('/posts/explore/')
