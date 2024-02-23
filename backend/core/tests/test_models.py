from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryAPITest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Category 1')

    def test_get_category(self):
        url = reverse('category-detail', args=[self.category.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CategorySerializer(self.category)
        self.assertEqual(response.data, serializer.data)


class ProductAPITest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Category 1')
        self.product = Product.objects.create(
            product_name='Product 1',
            slug='product-1',
            description='Product 1 description',
            information='Product 1 information',
            concise='Product 1 concise',
            color='ابی',
            size='XL',
            price=10.99,
            stock=100,
            discount=5,
            category=self.category
        )

    def test_get_product(self):
        url = reverse('product-detail', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ProductSerializer(self.product)
        self.assertEqual(response.data, serializer.data)
