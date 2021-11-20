''' Forms for our messages '''
from django import forms

class ThreadForm(forms.Form):
    ''' Form to create a thread '''
    username = forms.CharField(label='', max_length=100)

class MessageForm(forms.Form):
    ''' Form for the individual message '''
    message = forms.CharField(label='', max_length=1000)
