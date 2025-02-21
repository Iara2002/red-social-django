from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Comment, Like
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import FormView

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# Vista para ver la lista de publicaciones
class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'  # Debes crear este template
    context_object_name = 'posts'

# Vista para ver el detalle de una publicación
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'  # Debes crear este template
    context_object_name = 'post'

# Vista para crear una nueva publicación
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content', 'image']
    template_name = 'posts/post_create.html'  # Debes crear este template

    def form_valid(self, form):
        form.instance.user = self.request.user  # Asigna el usuario actual
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_list')

# Vista para crear un comentario
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'posts/comment_create.html'  # Debes crear este template

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.request.POST.get('post_id'))
        form.instance.user = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'id': self.object.post.id})

# Vista para dar o quitar "Me gusta"
from django.views import View

class LikeToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['id'])
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()  # Eliminar el "me gusta" si ya existía

        return JsonResponse({'likes_count': post.like_set.count()})
