from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.see_all_product, name='see_all_product'),
    path('products/<int:product_id>/', views.see_product_detail, name='see_product_detail'),
    path('products/update/<int:product_id>/', views.update_product, name='update_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
]
