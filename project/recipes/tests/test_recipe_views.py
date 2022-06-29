from http import HTTPStatus
from urllib import response

from django.test import TestCase
from django.urls import resolve, reverse
from project.recipes import views


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_views_function_is_correct(self):
        view = resolve(
            reverse(
                'recipes:category', kwargs={'category_id': 2}
            )
        )
        self.assertIs(view.func, views.category)

    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(
            reverse(
                'recipes:recipe', kwargs={'id': 5}
            )
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_home_status(self):
        response_get = self.client.get(reverse('recipes:home'))
        self.assertEqual(response_get.status_code, HTTPStatus.OK)

    def test_recipe_home_loads_correct_template(self):
        response_home = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response_home, 'recipes/pages/home.html')

    def test_recipe_home_templates_shows_no_recipes_found_no_recipes(self):
        response_templates = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found here',
            response_templates.content.decode('utf-8')
        )
