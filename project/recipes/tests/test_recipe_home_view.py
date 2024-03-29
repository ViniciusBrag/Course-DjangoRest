from http import HTTPStatus
from unittest.mock import patch

from django.urls import resolve, reverse
from project.recipes import views
from project.recipes.tests.test_recipe_base import RecipeBase


class RecipeHomeTest(RecipeBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_views_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 2}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 5}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_home_status_is_ok(self):
        response_get = self.client.get(reverse('recipes:home'))
        self.assertEqual(response_get.status_code, HTTPStatus.OK)

    def test_recipe_home_status_404(self):
        response_get_url = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 12})
        )
        self.assertEqual(response_get_url.status_code, HTTPStatus.NOT_FOUND)

    def test_recipe_home_loads_correct_template(self):
        response_home = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response_home, 'recipes/pages/home.html')

    def test_recipe_home_templates_shows_no_recipes_found_no_recipes(self):
        response_templates = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found here', response_templates.content.decode('utf-8')
        )

    def test_recipe_home_loads_recipe(self):
        """
        Check if one recipe_exists
        """
        self.make_recipe()
        response_loads = self.client.get(reverse('recipes:home'))
        content = response_loads.content.decode('utf-8')
        self.assertIn('Recipe title', content)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response_get_not_found = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(
            response_get_not_found.status_code, HTTPStatus.NOT_FOUND
        )

    def test_recipe_home_is_paginated(self):
        for i in range(9):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('project.recipes.views.PER_PAGE', new=3):
            response_paginated = self.client.get(reverse('recipes:home'))
            recipes = response_paginated.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
