from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .utils.lists import max_len


class Author(models.Model):
    sex = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    bio = models.TextField(max_length=110)
    birth = models.DateField(auto_now=False, auto_now_add=False, null=True)
    gender = models.CharField(choices=sex, max_length=max_len(sex))
    user = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    

    def get_absolute_url(self):
        return reverse("blogger:author_page", args=[self.username])

    @property
    def username(self):
        return self.user.username
    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        )
    
    author = models.ForeignKey(Author, related_name='posts', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=max_len(STATUS_CHOICES), default='draft')
    title = models.CharField(max_length=64)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique_for_date='publish')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blogger:view_post", args=[self.author, self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Author, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return f'Comment by {self.author.username}'