from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator


class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        (1, "Easy"),
        (2, "Medium"),
        (3, "Hard")
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.IntegerField(default='1', choices=DIFFICULTY_CHOICES)
    ingredients = models.ManyToManyField(Ingredient)
    image = models.ImageField(default='/default_recipe.jpeg', upload_to='recipe_pics')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'pk': self.pk})


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='likes', on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.recipe) + ':' + str(self.is_liked)

    class Meta:
        unique_together = ("user", "recipe")


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='rates', on_delete=models.CASCADE)
    points = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.recipe) + ':' + str(self.rate)

    class Meta:
        unique_together = ("user", "recipe")
