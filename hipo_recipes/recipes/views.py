from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count, FloatField
from django.db.models.functions import Cast
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Recipe, Ingredient, Like, Rate


def home(request):
    context = {
        'recipes': Recipe.objects.all()
    }
    return render(request, 'recipes/home.html', context)


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    ordering = ['-date_posted']


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'

    def get_queryset(self):
        return Recipe.objects.annotate(rate_average=Sum('rates__points') / Count('rates')).all()

    def get_object(self, queryset=None):
        recipe = super().get_object(queryset)
        recipe.like_count = recipe.likes.filter(is_liked=True).count()
        recipe.is_user_liked = recipe.likes.filter(user=self.request.user, is_liked=True).exists()
        if recipe.rates.filter(user=self.request.user).exists():
            recipe.user_rate = recipe.rates.get(user=self.request.user).points
        else:
            recipe.user_rate = None
        return recipe


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['title', 'content', 'image', 'difficulty', 'ingredients']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    fields = ['title', 'content', 'image', 'difficulty', 'ingredients']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = '/'

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    fields = ['name']
    success_url = '/recipes/create/'


@login_required
def like_recipe(request, pk):
    if request.method == "POST":
        recipe = Recipe.objects.get(pk=pk)
        like = recipe.likes.filter(user=request.user).first()
        if like:
            if like.is_liked:
                like.is_liked = False
                like.save()
            else:
                like.is_liked = True
                like.save()
        else:
            like = Like(user=request.user, recipe=recipe, is_liked=True)
            like.save()

        likes = recipe.likes.filter(is_liked=True).count()

        response = {
            "likes": likes,
            "is_liked": like.is_liked
        }
        return JsonResponse(response)


@login_required
def rate_recipe(request, pk):
    if request.method == "POST":
        recipe = Recipe.objects.get(pk=pk)
        rate = recipe.rates.filter(user=request.user).first()
        if rate:
            rate.points = int(request.POST['rate'])
            rate.save()
        else:
            rate = Rate(user=request.user, recipe=recipe, points=request.POST['rate'])
            rate.save()

        recipe = Recipe.objects.annotate(
            rate_average=Cast(Sum('rates__points'), FloatField()) / Cast(Count('rates'), FloatField())
        ).get(pk=pk)

        response = {
            "rate_average": recipe.rate_average,
            "user_rate": rate.points
        }
        return JsonResponse(response)
