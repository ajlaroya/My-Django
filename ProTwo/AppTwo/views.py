from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    my_dict = {'insert_help':"Help Page"}
    return render(request,'AppTwo/help.html',context=my_dict)
