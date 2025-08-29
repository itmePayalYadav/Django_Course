from django.urls import path
from .views import (
    articles_create_view, 
    articles_detail_view, 
    articles_update_view
)

urlpatterns = [
    path("create/", articles_create_view, name="article-create"),
    path("<int:id>/edit/", articles_update_view, name="article-update"), 
    path("<slug:slug>/", articles_detail_view, name="article-detail"),    
]
