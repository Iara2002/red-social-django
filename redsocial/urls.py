"""
URL configuration for redsocial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Importar views correctamente


urlpatterns = [
     path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Página de login
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Cierre de sesión
     path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('', views.PostListView.as_view(), name='home'),  # Redirigir la raíz a la lista de posts
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('comment/create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('like/<int:id>/', views.LikeToggleView.as_view(), name='like_toggle'),
]
