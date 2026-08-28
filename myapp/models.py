from django.db import models
from django.utils import timezone


class Member(models.Model):
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    avatar_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    dob = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    gender = models.CharField(max_length=20, blank=True)
    age = models.IntegerField(default=0)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    interests = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name or self.name


class Post(models.Model):
    author = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author}"
