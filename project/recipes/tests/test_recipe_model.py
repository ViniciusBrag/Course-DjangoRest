from django.core.exceptions import ValidationError
from parameterized import parameterized

from project.recipes.models import Recipe
from project.recipes.tests.test_recipe_base import RecipeBase


class RecipeModelTest(RecipeBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_default(self):
        recipe_test = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe title',
            description='Recipe Description',
            slug='recipe_slugs',
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=5,
            serving_unit='porções',
            preparation_steps='Recipe Preparation Steps',
        )
        recipe_test.full_clean()
        recipe_test.save()
        return recipe_test

    @parameterized.expand(
        [
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('serving_unit', 65),
        ]
    )
    def test_recipe_fields_max_lenght(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 2))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_step_is_html_is_false_by_default(self):
        recipe_preparation = self.make_recipe_no_default()
        self.assertFalse(
            recipe_preparation.preparation_steps_is_html,
            msg='Recipe preparation_steps_is_html is not False',
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe_is_published = self.make_recipe_no_default()
        self.assertFalse(
            recipe_is_published.is_published,
            msg='Recipe preparation_steps_is_html is not False',
        )

    def test_recipe_string_representation(self):
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing Representation')
