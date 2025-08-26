from . import views
from django.urls import path

urlpatterns = [
    path('', views.product_list_create_view, name="product-list"),
    path('<int:pk>/', views.product_detail_view, name="product-detail"),
    path('<int:pk>/edit/', views.product_edit_view, name="product-edit"),
    path('<int:pk>/destroy/', views.product_destroy_view, name="product-destroy"),
]
