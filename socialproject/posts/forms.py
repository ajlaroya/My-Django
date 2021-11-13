from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    message = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))
    class Meta:
        model = Post
        fields = ['message']

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
