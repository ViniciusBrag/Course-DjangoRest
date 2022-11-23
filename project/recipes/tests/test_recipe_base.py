from django.test import TestCase

from project.recipes.models import Category, Recipe, User

# classe que existe metodos que outras classes não tem relação, apenas para transferir métodos para outra classe


class RecipeMixin:
    def make_category(self, name='Category test'):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='UserFake',
        last_name='name',
        username='username',
        password='1234566',
        email='username@email.com',
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='Recipe title',
        description='Recipe Description',
        slug='recipe_slug',
        preparation_time=10,
        preparation_time_unit=3,
        servings=5,
        serving_unit='porções',
        preparation_steps='Recipe Preparation Steps',
        preparation_steps_is_html=False,
        is_published=True,
    ):

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            serving_unit=serving_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )


class RecipeBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
