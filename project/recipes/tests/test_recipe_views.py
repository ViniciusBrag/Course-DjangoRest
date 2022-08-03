from http import HTTPStatus

from django.urls import resolve, reverse

from project.recipes import views
from project.recipes.tests.test_recipe_base import RecipeBase


class RecipeViewsTest(RecipeBase):
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

    def test_recipe_search_uses_correct_view_function(self):
        resolved_view = resolve(reverse('recipes:search'))
        self.assertIs(resolved_view.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response_search = self.client.get(
            reverse('recipes:search') + '?q=teste'
        )
        self.assertTemplateUsed(response_search, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response_search_term = self.client.get(reverse('recipes:search'))
        self.assertEqual(
            response_search_term.status_code, HTTPStatus.NOT_FOUND
        )

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url_search = reverse('recipes:search') + '?q=<Teste>'
        response_url_search = self.client.get(url_search)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response_url_search.content.decode('utf-8'),
        )
