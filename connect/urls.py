from django.urls import path
from . import views

app_name = 'connect'
urlpatterns = [
    path('contact/', views.ContactView.as_view(), name='contact'),
    # path('about/', views.AboutView.as_view(), name='about'),
    path('creators/', views.CreatorView.as_view(), name='creators'),
]
