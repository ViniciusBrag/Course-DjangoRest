from django.urls import reverse
from project.recipes.tests.test_recipe_base import RecipeBase


class RecipeSearchViewTest(RecipeBase):
    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8'),
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe_search_one = self.make_recipe(
            slug='one',
            title=title1,
            author_data={'username': 'one'},
        )

        recipe_search_two = self.make_recipe(
            slug='two',
            title=title2,
            author_data={'username': 'two'},
        )

        search_url = reverse('recipes:search')
        response_1 = self.client.get(f'{search_url}?q={title1}')
        response_2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe_search_one, response_1.context['recipes'])
        self.assertNotIn(recipe_search_two, response_1.context['recipes'])

        self.assertIn(recipe_search_two, response_2.context['recipes'])
        self.assertNotIn(recipe_search_one, response_2.context['recipes'])

        self.assertIn(recipe_search_one, response_both.context['recipes'])
        self.assertIn(recipe_search_two, response_both.context['recipes'])
