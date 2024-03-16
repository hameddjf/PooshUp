from django.urls import path
from .views import cart, add_cart, remove_cart, delete_cart_item, checkout

app_name = 'cart'
urlpatterns = [
    path('', cart, name='cart_page'),
    path('add_to_cart/<int:product_id>/', add_cart, name='add_to_cart_page'),
    path('remove_from_cart/<int:product_id>/<int:cart_item_id>/',
         remove_cart, name='remove_from_cart_page'),
    path('delete_cart_item/<int:product_id>/<int:cart_item_id>/',
         delete_cart_item, name='delete_cart_item_page'),

    path('checkout/', checkout, name='checkout_page')
]
