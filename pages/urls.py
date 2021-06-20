from django.contrib.auth import views
from django.urls import path, reverse_lazy

from .views import *
from .utils.staff import staff_path

app_name = 'blogger'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contact', ContactView.as_view(), name='contact'),
    path('@<author>/', AuthorView.as_view(), name='author_page'),
    path('home/', HomeView.as_view(), name='home'),
    path("accounts/login/", views.LoginView.as_view(template_name='login.html'), name="login"),
    path("accounts/logout", views.LogoutView.as_view(), name="logout"),
    path('accounts/create/', UserRegistrationView.as_view(), name='create_user'),
    path('accounts/settings/', SettingsView.as_view(), name='profile_settings'),
    path('accounts/settings/password', views.PasswordChangeView.as_view(template_name='settings/password_change.html', success_url=reverse_lazy('blogger:password_change_done')), name='password_change'),
    path('accounts/settings/password/done', views.PasswordChangeDoneView.as_view(template_name='settings/password_done.html'), name='password_change_done'),
    path('accounts/settings/info', InfoUpdateView.as_view(), name='profile_update'),
    path('@<author>/<slug:slug>', PostView.as_view(), name='view_post',),
    path('home/post/create', CreatePostView.as_view(), name='create_post'),
    path('search', SearchView.as_view(), name='search_detail'),
    staff_path('dashboard', DashboardView.as_view, login_url='blogger:login', name='dashboard'),
]
