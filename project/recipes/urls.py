from django.urls import path
from project.recipes.views import home

urlpatterns = [
    path('', home, name='home'),

]
