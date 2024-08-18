from django.urls import path
from . import views

app_name = 'discount'

urlpatterns = [
    path('', views.DiscountListView.as_view(), name='discount_list'),
    path('<int:pk>/', views.DiscountDetailView.as_view(), name='discount_detail'),
]
