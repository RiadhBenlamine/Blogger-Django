from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class':'form-control',
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        }
    ))

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'status']
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body',]

class SearchForm(forms.Form):
    search = forms.CharField(max_length=80, widget=forms.TextInput(attrs={
        'class':'form-control',
        'type':'search',
        }
    ))

    def search_author(self, query):
        authors = User.objects.filter(username__contains=query)
        return authors

    def search_post(self, query):
        posts = Post.objects.filter(title__contains=query)
        return posts