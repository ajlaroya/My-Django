from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
            })
        )

    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True
            })
        )

    class Meta:
        model = Post
        fields = ['message','image']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Comment...'}
        ))
    class Meta:
        model = Comment
        fields = ['comment']

class ShareForm(forms.Form):
    ''' Handles ability for user to enter text with a shared post '''
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
            })
        )
