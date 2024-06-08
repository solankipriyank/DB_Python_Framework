from django.urls import path
from . import views

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('add_product_subcat/', views.add_product_subcat, name='add_product_subcat'),
    path('products/', views.product_list, name='product_list'),
    path('search_products/', views.search_products, name='search_products'),
    path('update_product_subcat/<int:sub_cat_id>/', views.update_product_subcat, name='update_product_subcat'),
    path('delete_product_subcat/<int:sub_cat_id>/', views.delete_product_subcat, name='delete_product_subcat'),
]
