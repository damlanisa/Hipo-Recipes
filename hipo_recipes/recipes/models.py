from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'pk': self.pk})
