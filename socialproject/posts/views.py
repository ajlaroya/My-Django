from django.shortcuts import render, redirect
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

        context = {
            'post_list': posts,
            'form': form,
            'shareform': share_form,
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

class UserPosts(generic.ListView):
    model = Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(
                username__iexact=self.kwargs.get('username')
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-timestamp')
        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'posts/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            new_comment.create_tags()

        comments = Comment.objects.filter(post=post).order_by('-timestamp')

        notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'posts/post_detail.html', context)

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    fields = ('message','group','image')
    model = Post

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = Post
    select_related = ('author','group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author_id = self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)

class EditPost(LoginRequiredMixin,SelectRelatedMixin,generic.UpdateView):
    model = Post
    select_related = ('author',)
    fields = ['message']
    template_name = 'posts/post_edit.html'

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

class CommentReplyView(LoginRequiredMixin, generic.View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)
        notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        return redirect('posts:single', username=post.author, pk=post_pk)

class CommentDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Comment
    template_name = 'posts/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('posts:single', kwargs={'pk': pk, 'username':self.request.user})

class AddCommentLike(LoginRequiredMixin, generic.View):
    def post(self, request, post_pk, pk, *args, **kwargs):
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
          'shareform':share_form
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
