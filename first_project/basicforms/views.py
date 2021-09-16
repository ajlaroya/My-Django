from django.shortcuts import render
from basicforms import forms

# Create your views here.
def form_view(request):
    form = forms.FormName
    return render(request,'basicforms/form_page.html',{'form':form})
