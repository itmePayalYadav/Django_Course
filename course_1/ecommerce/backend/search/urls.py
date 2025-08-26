from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_list_view, name="search"),
]
