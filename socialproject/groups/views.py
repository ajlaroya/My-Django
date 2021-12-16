from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from braces.views import SelectRelatedMixin
from groups.models import Group,GroupMember
from posts.models import Post, Image
from posts.forms import PostForm, CommentForm
from .forms import GroupForm
from . import models

# Create your views here.

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    model = Group
    form_class = GroupForm

    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super().form_valid(form)

# Might need to add loginrequiredmixin
class SingleGroup(FormMixin, generic.DetailView):
    model = Group
    template_name = 'groups/group_detail.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs.get('slug')
        context['reply_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.group = Group.objects.get(slug=self.kwargs.get('slug'))
            new_post.save()

            new_post.create_tags()

            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()

        context = {
            'slug': self.kwargs.get('slug'),
            'form': form
        }

        return redirect(reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')}))
        # return render(request, 'groups/group_detail.html', context)

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)

        except:
            messages.warning(self.request,'Warning already a member!')

        else:
            messages.success(self.request,'You are now a member!')

        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,'You are not in this group')

        else:
            membership.delete()
            messages.success(self.request,'You have left the group!')

        return super().get(request,*args,**kwargs)

class EditGroup(LoginRequiredMixin,SelectRelatedMixin,generic.UpdateView):
    model = Group
    select_related = ('admin',)
    fields = ['name','description']
    template_name = 'groups/group_edit.html'

class DeleteGroup(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = Group
    select_related = ('admin',)
    success_url = reverse_lazy('groups:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(admin_id = self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Group Deleted')
        return super().delete(*args,**kwargs)
