from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView
from django.http import HttpResponse
from . import models # . = look at CWD

# CLASS BASED VIEWS /

# class CBView(View):
#     def get(self,request):
#         return HttpResponse('Class based views are cool!')

# class IndexView(TemplateView):
#     template_name = 'index.html'
#
#     def get_context_data(self,**kwargs): # keyword arguments
#         context = super().get_context_data(**kwargs)
#         context['injectme'] = 'BASIC INJECTION'
#         return context

class SchoolListView(ListView):
    context_object_name = 'schools'
    model = models.School

class SchoolDetailView(DetailView):
    context_object_name = 'school_detail'
    model = models.School
    template_name = 'basic_app/school_detail.html'
