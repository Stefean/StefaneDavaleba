from django.urls import path
from . import views

urlpatterns = [
    path("", views.recipe_list, name="list"),
    path("<int:pk>", views.recipe_detail, name="detail"),
    path("category/<str:name>/", views.category_detail, name="category"),
    path("search/", views.search, name="category"),
    path("random/", views.random_recipe, name = "random_recipe"),
    path("details/<str:slug>/", views.recipe_by_slug, name="recipe_by_slug"),
]
