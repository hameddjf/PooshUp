from django.urls import path
from .views import place_order, payments, order_complete

app_name = 'order'
urlpatterns = [
    path('place_order/', place_order, name='place_order_page'),
    path('payments/', payments, name='payments_page'),
    path('order_complete/', order_complete, name='order_complete_page'),
]
