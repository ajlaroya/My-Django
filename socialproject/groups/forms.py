from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'rows': '6', 'placeholder':'Group name',
            'class': 'control is-warning textarea mb-3'
            })
        )

    description = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '6', 'placeholder':'Description of group',
            'class': 'control is-warning textarea mb-3'
            })
        )

    class Meta:
        model = Group
        fields = ['name','description']
