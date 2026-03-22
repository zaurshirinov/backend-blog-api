from django.contrib import admin

from .models import Post, Comment, Profile, Category


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)
