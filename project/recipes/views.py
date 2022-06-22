from django.shortcuts import render
from project.recipes.models import Recipe
from utils.recipes.factory import make_recipe


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def recipe(request, id):
    return render(request, 'recipes/pages/recipe_view.html', context={
        'recipe': make_recipe(),
        'is_detail_page': True,

    })


def category(request, category_id):
    recipes = Recipe.objects.filter(
        is_published=True,
        category__id=category_id
    ).order_by('-id')
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
    })
