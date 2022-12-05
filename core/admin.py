from django.contrib import admin
from .models import Profile, Post, Follow, Like
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Like)