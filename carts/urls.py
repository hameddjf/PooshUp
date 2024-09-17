from django.urls import path
from .views import CartView, remove_cart, delete_cart_item, CheckoutView

app_name = 'cart'
urlpatterns = [
    path('', CartView.as_view(), name='cart_page'),
    path('add_to_cart/<int:product_id>/',
         CartView.as_view(), name='add_to_cart_page'),
    path('remove_from_cart/<int:product_id>/<int:cart_item_id>/',
         remove_cart, name='remove_from_cart_page'),
    path('delete_cart_item/<int:product_id>/<int:cart_item_id>/',
         delete_cart_item, name='delete_cart_item_page'),

    path('checkout/', CheckoutView.as_view(), name='checkout_page')
]
