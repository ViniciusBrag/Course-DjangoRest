
import pytest
from selenium.webdriver.common.by import By

from tests.recipes.base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePage(RecipeBaseFunctionalTest):

    def test_recipe_home_page_withoud_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here', body.text)
