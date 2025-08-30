from django.urls import path
from django.contrib import admin
from .views import (
    recipe_list_view,
    recipe_create_view,
    recipe_detail_view,
    recipe_update_view,
    recipe_detail_hx_view,
    recipe_ingredient_update_hx_view
)

urlpatterns = [
    path("", recipe_list_view, name="recipe-list"),  
    path("create/", recipe_create_view, name="recipe-create"),
    path("<slug:slug>/", recipe_detail_view, name="recipe-detail"),  
    path("<int:id>/edit/", recipe_update_view, name="recipe-update"),  
    path("hx/<slug:slug>/", recipe_detail_hx_view, name="recipe-detail-hx"),
    path("hx/<slug:slug>/ingredient/<int:id>/", recipe_ingredient_update_hx_view, name="recipe-ingredient-update-hx"),
]
