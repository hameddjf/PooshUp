from django.urls import path
from .views import LikeItemView

app_name = 'like'

urlpatterns = [
    path('like/<int:product_id>/', LikeItemView.as_view(), name='like_item'),
]
