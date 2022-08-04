from http import HTTPStatus

from django.urls import reverse

from project.recipes.tests.test_recipe_base import RecipeBase


class RecipeDetailViewTest(RecipeBase):
    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)

        response_category = self.client.get(
            reverse('recipes:category', args=(1,))
        )
        content_category = response_category.content.decode('utf-8')

        self.assertIn(needed_title, content_category)

    def test_recipe_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load one recipe'

        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response_category = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        content_category = response_category.content.decode('utf-8')

        self.assertIn(needed_title, content_category)

    def test_recipe_home_template_dont_loads_recipe_not_published(self):
        """
        Test recipe is published True
        """
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response_not_published = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.category.id})
        )
        self.assertEqual(
            response_not_published.status_code, HTTPStatus.NOT_FOUND
        )

    def test_recipe_detail_template_dont_loads_recipe_not_published(self):
        """
        Test recipe is published False dont show
        """
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response_not_published = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id})
        )
        self.assertEqual(
            response_not_published.status_code, HTTPStatus.NOT_FOUND
        )
