from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, View, ListView


from .forms import *
from .models import *

class IndexView(ListView):
    template_name = "index.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status='published')

class AuthorView(View):
    template_name = 'author.html'

    def get(self, request, author):
        user = get_object_or_404(User, username=author)
        posts = user.author.get().posts.all().filter(status='published')
        context = {
            'posts': posts,
            'author':user.author.get()
            }
        return render(request, self.template_name, context=context)

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = reverse_lazy('blogger:login')
    redirect_field_name = 'go_to'

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'settings/settings.html'

class InfoUpdateView(LoginRequiredMixin, View):
    model = Author
    form_klass = ChangeUserInfoForm
    template_name = 'settings/info_change.html'
    def get(self, request):
        author = Author.objects.get(id=request.user.author.get().id)
        form = self.form_klass()
        context = {
            'form':form
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        author = Author.objects.get(id=request.user.author.get().id)
        user = User.objects.get(id=request.user.id)
        form = self.form_klass(request.POST)
        if form.is_valid():
            user.username = form.data['username']
            author.gender = form.data['gender']
            author.birth = form.data["birth"]
            author.bio = form.data['bio']
            user.save()
            author.save()
        context = {
            'form':form
        }
        
        return redirect(reverse_lazy('blogger:home'))

class ContactView(TemplateView):
    template_name = 'contact.html'

class UserRegistrationView(View):
    template_name = 'register_user.html'
    form = UserCreationForm
    success_url = reverse_lazy('blogger:login')
    
    def get(self, request):
        form = self.form()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User(
                username=cd['username'],
            )
            user.set_password(cd['password1'])
            user.save()
            author = Author(
                pk=user.pk,
                user=user
            )
            author.save()
            return redirect(self.success_url)
        return render(request, self.template_name, context={'form':form})
    
class PostView(View):
    model = Post
    form_klass = CommentForm
    template_name = "post.html"

    def get(self, request, author, slug):
        ''' Forgot to extend user but this gonna work '''
        author = get_object_or_404(User, username=author)
        post = get_object_or_404(
            self.model,
            slug=slug,
            author=author.id,
            status='published'
        )
        comments = post.comments.all()
        form = self.form_klass()
        context = {
            'post': post,
            'comments': comments,
            'form': form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, author, slug):
        author = get_object_or_404(User, username=author)
        post = get_object_or_404(
            self.model,
            slug=slug,
            author=author.id,
            status='published'
        )
        comments = post.comments.all()
        form = self.form_klass(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user.author.get()
            new_comment.save()
        context = {
            'post': post,
            'comments': comments,
            'form':form,
        }
        return render(request, self.template_name, context=context)


class CreatePostView(LoginRequiredMixin, View):
    model = Post
    template_name = 'create_post.html'
    form_klass = CreatePostForm

    def get(self, request):
        context = {
            'form': self.form_klass,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        context = {
            'form': self.form_klass,
        }
        form = self.form_klass(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user.author.get()
            new_post.slug = form.cleaned_data['title'].replace(' ', '-')
            new_post.save()
        
        return render(request, self.template_name, context=context)

class SearchView(View):
    template_name = 'search.html'
    form_klass = SearchForm

    def get(self, request):
        form = self.form_klass()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        form = self.form_klass(request.POST)
        if form.is_valid():
            posts = form.search_post(form.cleaned_data['search'])
            authors = form.search_author(form.cleaned_data['search']) 
            context = {
                'form':form,
                'authors':authors,
                'posts':posts,
            }
            return render(request, self.template_name, context=context)
        
        context = {
            'form':form,
            'authors': [],
            'posts': [],
        }
        return render(request, self.template_name, context=context)

class DashboardView(LoginRequiredMixin, View):
    model = Author
    template_name = 'dashboard.html'
    def get(self, request):

        users = Author.objects.all()
        posts = Post.objects.all()
        context = {
           'total_users' : len(users),
           'total_posts': len(posts),
        }
        return render(request, self.template_name, context=context)