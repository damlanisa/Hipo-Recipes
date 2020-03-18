from django.urls import path
from . import views
from .views import (
    RecipeListView,
    RecipeDetailView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    IngredientCreateView
)


urlpatterns = [
    path('', RecipeListView.as_view(), name='recipes-home'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipes/create/', RecipeCreateView.as_view(), name='recipe-create'),
    path('recipes/<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe-update'),
    path('recipes/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe-delete'),
    path('recipes/<int:pk>/like/', views.like_recipe, name='recipe-like'),
    path('recipes/<int:pk>/rate/', views.rate_recipe, name='recipe-rate'),
    path('ingredients/create/', IngredientCreateView.as_view(), name='ingredient-create'),
]
