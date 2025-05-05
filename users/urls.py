from django.urls import path
from .views import register_view, profile_view, user_list_view, public_profile_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = 'login'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('', user_list_view, name = 'user-list'),
    path('<str:username>/', public_profile_view, name='public-profile'),
]