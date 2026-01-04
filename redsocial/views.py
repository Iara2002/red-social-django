from django.shortcuts import render, get_object_or_404, redirect
<<<<<<< HEAD
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from django.views import View
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms

from .models import Post, Comment, Like, UserProfile


@login_required
def profile_view(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-created_at')

    return render(request, 'profile/profile.html', {
        'user': user,
        'posts': posts
    })
=======
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Comment, Like
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import FormView
>>>>>>> 5b63707d3d425c608cb326254d8b17b22bea0273

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

<<<<<<< HEAD

# Lista de publicaciones
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


# Detalle de publicación
class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # Likes
        context['likes_count'] = post.like_set.count()
        if self.request.user.is_authenticated:
            context['user_has_liked'] = Like.objects.filter(
                post=post,
                user=self.request.user
            ).exists()
        else:
            context['user_has_liked'] = False

        return context


# Crear publicación
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content', 'image']
    template_name = 'posts/post_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
=======
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
>>>>>>> 5b63707d3d425c608cb326254d8b17b22bea0273
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_list')

<<<<<<< HEAD

# EDITAR publicación
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content', 'image']
    template_name = 'posts/post_edit.html'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return post.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


# CREAR comentario
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'posts/comment_create.html'
=======
# Vista para crear un comentario
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'posts/comment_create.html'  # Debes crear este template
>>>>>>> 5b63707d3d425c608cb326254d8b17b22bea0273

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.request.POST.get('post_id'))
        form.instance.user = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
<<<<<<< HEAD
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.id})


# EDITAR comentario
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'posts/comment_edit.html'
    context_object_name = 'comment'

    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})


# Me gusta / quitar me gusta
class LikeToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()  # si ya existía, lo borramos

        return redirect('post_detail', pk=post.pk)


# Eliminar publicación
class PostDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # Solo el autor puede borrar
        if post.user != request.user:
            return redirect('post_detail', pk=pk)

        post.delete()
        return redirect('post_list')


# Eliminar comentario
class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        # Solo el autor puede borrar
        if comment.user != request.user:
            return redirect('post_detail', pk=comment.post.pk)

        post_id = comment.post.pk
        comment.delete()
        return redirect('post_detail', pk=post_id)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']

@method_decorator(login_required, name='dispatch')
class ProfileEditView(UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'profile/profile_edit.html'

    def get_object(self):
        return self.request.user.userprofile

    def get_success_url(self):
        return reverse_lazy('profile')
    
# ------------------ PERFIL DE USUARIO ------------------ #

@login_required
def profile_view(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-created_at')

    return render(request, 'profile/profile.html', {
        'user': user,
        'posts': posts,
    })


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']


@method_decorator(login_required, name='dispatch')
class ProfileEditView(UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'profile/profile_edit.html'

    def get_object(self):
        return self.request.user.userprofile

    def get_success_url(self):
        return reverse_lazy('profile')
=======
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
>>>>>>> 5b63707d3d425c608cb326254d8b17b22bea0273
