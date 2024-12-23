from django.urls import path
from .views import PlaceOrderView, PaymentCallbackView, PaymentView, GoToGatewayView, OrderCompleteView

app_name = 'order'
urlpatterns = [
    path('place_order/', PlaceOrderView.as_view(), name='place_order_page'),
    # path('payments/', payments, name='payments_page'),
    path('order_complete/', OrderCompleteView.as_view(),name='order_complete_page'),

    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment-callback/', PaymentCallbackView.as_view(),name='payment_callback'),
    path('go-to-gateway/', GoToGatewayView.as_view(), name='go_to_gateway'),
]
