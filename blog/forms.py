from django import forms
from django.contrib.auth.models import User
from .models import Blog
from .models import Comment


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content','image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

