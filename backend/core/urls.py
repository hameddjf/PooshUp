from django.urls import path
from .views import (
    home,
    ProductList,
    ProductDetail,
    product,
    product_detail,
)

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('products/category/<slug:category_slug>/',
         product, name='product-by-category'),
    path('products/category/<slug:category_slug>/<slug:product_slug>/',
         product_detail, name='product-detail-by-category'),
]
