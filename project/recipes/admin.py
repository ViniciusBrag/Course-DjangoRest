from django.contrib import admin

from project.recipes.models import Category, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
