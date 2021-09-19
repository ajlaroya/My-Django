from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

def register(request):
    registered = False # check if registered

    if request.method == "POST":
        user_form = UserForm(data=request.POST) # grab info from forms
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() # if valid, grabs data from user form
            user.set_password(user.password) # hash password
            user.save() # saves user to database

            profile = profile_form.save(commit=False) # grabs data from profile form
            profile.user = user

            if 'profile_pic' in request.FILES: # checks pic before saving
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()  # saves profile to database

            registered = True # sets registered to true

        else:
            print(user_form.errors,profile_form.errors) # if invalid print errors

    else: # if request is not POST, sets forms
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})
