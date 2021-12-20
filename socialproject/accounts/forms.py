''' Forms for our messages '''
from django import forms
from .models import MessageModel, UserProfile, Contact

class ThreadForm(forms.Form):
    ''' Form to create a thread '''
    username = forms.CharField(label='', max_length=100,
        widget=forms.TextInput(attrs={'placeholder':'Username',
        'class': 'is-warning is-rounded'}))

class MessageForm(forms.ModelForm):
    ''' Form for the individual message '''
    body = forms.CharField(label='', max_length=1000,
        widget=forms.TextInput(attrs={'placeholder':'Say something',
        'class':'is-warning is-rounded mb-5'}))
    image = forms.ImageField(label='Send an Image', required=False,)

    class Meta:
        model = MessageModel
        fields = ['body', 'image']

class ProfileEditForm(forms.ModelForm):
    bio = forms.CharField(label='Bio:', max_length=500,
        widget=forms.Textarea(attrs={'rows': '10',
        'class':'text-area is-warning mb-5'}))

    location = forms.CharField(label='Location:', max_length=100,
        widget=forms.TextInput(attrs={'placeholder':'Location',
        'class':'is-warning mb-5'}))

    picture = forms.ImageField(required=False,
        widget=forms.FileInput(attrs={'class':'file-input has-name'}))

    class Meta:
        model = UserProfile
        fields = ['bio','location','picture']

class ContactForm(forms.ModelForm):
    email = forms.CharField(label='', max_length=100,
        widget=forms.TextInput(attrs={'placeholder':'Your email',
        'class': 'is-warning mb-3'}))

    subject = forms.CharField(label='', max_length=100,
        widget=forms.TextInput(attrs={'placeholder':'Subject ',
        'class': 'is-warning mb-3'}))

    message = forms.CharField(label='', max_length=500,
        widget=forms.Textarea(attrs={'placeholder':'Message','rows': '10',
        'class':'text-area is-warning mb-3'}))

    class Meta:
        model = Contact
        fields = '__all__'
