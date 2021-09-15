from django.shortcuts import render
from django.http import HttpResponse
from AppTwo.models import User

# Create your views here.
def index(request):
    return HttpResponse("<h1>Welcome!</h1><h2>Go to /users to see a list of user information!</h2>")

def help(request):
    my_dict = {'insert_help':"Help Page"}
    return render(request,'AppTwo/help.html',context=my_dict)

def users(request):
    user_list = User.objects.order_by('first_name')
    user_dict = {'users':user_list}
    return render(request,'AppTwo/users.html',context=user_dict)
