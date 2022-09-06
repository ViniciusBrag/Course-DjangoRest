import os

from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from project.recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(
        request,
        'recipes/pages/home.html',
        context={
            'recipes': page_obj,
            'pages': pagination_range,
        })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )
    page_obj, pagiantion_range = make_pagination(request, recipes, PER_PAGE)

    return render(
        request,
        'recipes/pages/category.html',
        context={
            'recipes': page_obj,
            'pagiantion_range': pagiantion_range,
            'title': f'{recipes[0].category.name} - Category | ',
        },
    )


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(
        request,
        'recipes/pages/recipe_view.html',
        context={
            'recipe': recipe,
            'is_detail_page': True,
        },
    )


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        # busca no banco de dados o termo digitado pelo usuário, que pode está entre o termo buscado, por isso "icontains" ignorando qualquer tipo de 'case' no
        Q(title__icontains=search_term) |
        Q(description__icontains=search_term),
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(
        request,
        'recipes/pages/search.html',
        {
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'recipes': page_obj,
            'pagiantion_range': pagination_range,
            'additional_url_query': f'&q={search_term}',
        },
    )
