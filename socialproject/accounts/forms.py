''' Forms for our messages '''
from django import forms
from .models import MessageModel

class ThreadForm(forms.Form):
    ''' Form to create a thread '''
    username = forms.CharField(label='', max_length=100)

class MessageForm(forms.ModelForm):
    ''' Form for the individual message '''
    body = forms.CharField(label='', max_length=1000)
    image = forms.ImageField(label='Send an Image', required=False)

    class Meta:
        model = MessageModel
        fields = ['body', 'image']
