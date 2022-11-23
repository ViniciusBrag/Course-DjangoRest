from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from project.recipes.tests.test_recipe_base import RecipeMixin
from utils.browser import make_browser


class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_browser()
        return super().setUp()

    def sleep(self, seconds=5):
        sleep(seconds)

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
