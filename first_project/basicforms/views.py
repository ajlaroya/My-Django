from django.shortcuts import render
from basicforms import forms

# Create your views here.
def form_view(request):
    form = forms.FormName

    if request.method == 'POST':
        form = forms.FormName(request.POST)

        if form.is_valid():
            print("Validation Success!")
            print("Name: "+form.cleaned_data['name'])
            print("Email: "+form.cleaned_data['email'])
            print("Text: "+form.cleaned_data['text'])

    return render(request,'basicforms/form_page.html',{'form':form})
