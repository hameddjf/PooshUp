from rest_framework import generics
from django.shortcuts import render, get_object_or_404

from .models import Product, Category
from .serializers import CategorySerializer, ProductSerializer
# Create your views here.


def home(request):
    products = Product.objects.filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request, 'index.html', context)


class ProductList(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer


def product(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    serializer = CategorySerializer(categories, many=True)

    context = {
        'categories': serializer.data,
        'products': products,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(
        Product, category__slug=category_slug, slug=product_slug)

    context = {
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)
