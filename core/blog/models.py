from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
    )
    profile_photo = models.ImageField(upload_to="profiles/")


class Post(models.Model):
    author = models.ForeignKey(
        User, 
        related_name="posts", 
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        related_name="comments", 
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
