from django import forms
from .models import Post, Comment
from groups.models import Group

class PostForm(forms.ModelForm):
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3', 'placeholder':'Say something!',
            'class': 'control is-warning textarea mb-3'
            })
        )

    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True,
            })
        )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label='Group',
        required=False,
        widget=forms.Select(attrs={
            'class': 'mb-3 control'
            })
        )

    class Meta:
        model = Post
        fields = ['message','group','image']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3','placeholder':'Got something to comment?',
            'class': 'is-warning textarea'}
        ))
    class Meta:
        model = Comment
        fields = ['comment']

class ShareForm(forms.Form):
    ''' Handles ability for user to enter text with a shared post '''
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3','placeholder':'Got something to share?',
            'class': 'is-warning textarea'
            })
        )

class ExploreForm(forms.Form):
    ''' Search form to filter explore page by other tags
    allowing users to search for posts with specific tags '''
    query = forms.CharField(
    label='',
    widget=forms.TextInput(attrs={'placeholder':'Enter hashtag',
        'class': 'is-warning is-rounded'})
    )
