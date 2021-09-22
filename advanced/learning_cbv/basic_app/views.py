from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponse

# Class based views!

# class CBView(View):
#     def get(self,request):
#         return HttpResponse('Class based views are cool!')

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self,**kwargs): # keyword arguments
        context = super().get_context_data(**kwargs)
        context['injectme'] = 'BASIC INJECTION'
        return context
