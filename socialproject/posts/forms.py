from django import forms

class PostForm(forms.Form):
    message = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': "input-lg"}),
    )
