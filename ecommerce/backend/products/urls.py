from . import views
from django.urls import path

urlpatterns = [
    path('', views.product_list_create_view),
    path('<int:pk>/', views.product_detail_view),
    path('<int:pk>/edit/', views.product_edit_view),
    path('<int:pk>/destroy/', views.product_destroy_view),
]
