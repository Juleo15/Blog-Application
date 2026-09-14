from django import forms
from .models import Post

# class PostForm(forms.forms):
#     title = forms.CharField(max_length=100)
#     content = forms.CharField(widget=forms.Textarea)
#     author = forms.CharField(max_length=100)
#     status = forms.ChoiceField(max_length=100)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'status']
