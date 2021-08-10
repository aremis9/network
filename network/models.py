from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin

class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(User, blank=False, related_name="likers")

    def __str__(self):
        return f"Post {self.id} by {self.poster} ({self.likes} likes)"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    followers = models.ManyToManyField(User, blank=False, related_name="followers")
    following = models.ManyToManyField(User, blank=False, related_name="following")



class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "poster", "timestamp")


class FollowAdmin(admin.ModelAdmin):
    list_display = ("user",)