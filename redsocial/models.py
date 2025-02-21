from django.db import models
from django.contrib.auth.models import User  # Importamos el modelo de usuario de Django

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    content = models.TextField()  # Contenido del post
    image = models.ImageField(upload_to="posts/", blank=True, null=True)  # Imagen opcional
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return f"Post de {self.user.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Relación con el post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Autor del comentario
    content = models.TextField()  # Texto del comentario
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return f"Comentario de {self.user.username} en {self.post.id}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Relación con el post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que dio like
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha del like

    def __str__(self):
        return f"Like de {self.user.username} en {self.post.id}"