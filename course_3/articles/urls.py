from django.urls import path
from django.contrib import admin
from .views import articles_create_view, articles_detail_view

urlpatterns = [
    path("create/", articles_create_view, name="article-create"),
    path("<str:pk>/", articles_detail_view, name="article-detail"),
]
