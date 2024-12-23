from django.urls import path
from .views import (
    register, login, logout, activate, profile,
    forgot_password, reset_password_validate, reset_password,
    MyOrdersView, edit_profile, change_password, order_detail)

app_name = 'account'
urlpatterns = [
    path('register/', register, name=("register_page")),
    path('login/', login, name=("login_page")),
    path('logout/', logout, name=("logout_page")),
    path('profile/', profile, name=("profile_page")),

    path('forgot-password/', forgot_password, name=("forgot_password_page")),
    path('reset-password/', reset_password, name=("reset_password_page")),
    path('activate/<uidb64>/<token>/', activate, name=("activate_page")),
    path('reset-password-validate/<uidb64>/<token>/',
         reset_password_validate, name=("reset_password_validate_page")),

    path('my_orders/', MyOrdersView.as_view(), name='my_orders_page'),
    path('edit_profile/', edit_profile, name='edit_profile_page'),
    path('change_password/', change_password, name='change_password_page'),
    path('order_detail/<int:order_id>/',
         order_detail, name='order_detail_page'),

]
