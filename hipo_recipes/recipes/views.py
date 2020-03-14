from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Recipe, Ingredient


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


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['title', 'content', 'ingredients']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    fields = ['title', 'content']

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
