from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, blank=True)
    age = models.IntegerField(default=0)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    interests = models.TextField(blank=True)

    def __str__(self):
        return self.name
