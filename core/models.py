from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userid = models.IntegerField()
    bio = models.TextField(default="",blank=True, max_length=300, null=True)
    profile_picture = models.ImageField(upload_to="profile_images", default="default.jpg")

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=30)
    image = models.ImageField(upload_to="post_images" ,default='defualt.jpg')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=datetime.now)
    likes = models.IntegerField(default=0)
    post_event = models.CharField(max_length=40, default="other")

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.user + " - " + self.title 

class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    follower = models.CharField(default="admin", max_length=40)
    following = models.CharField(default="admin", max_length=40)
    def __str__(self)->str:
        return self.follower + " -> " + self.following

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    def __str__(self)->str:
        return self.post_id + " -> " + self.username
