from django.urls import reverse
from django.test import TestCase, RequestFactory
from rest_framework.test import APIRequestFactory, APITestCase
from ..models import Category, Product
from ..views import home, ProductList, ProductDetail
from ..serializers import ProductSerializer, CategorySerializer
import pprint


class HomeViewTest(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class ProductListViewTest(APITestCase):
    def test_product_list_view(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('product-list'))
        view = ProductList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


class ProductDetailViewTest(APITestCase):
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

    def test_product_detail_view(self):
        factory = APIRequestFactory()
        request = factory.get(
            reverse('product-detail', args=[self.product.pk]))
        view = ProductDetail.as_view()
        response = view(request, pk=self.product.pk)
        self.assertEqual(response.status_code, 200)


class ProductViewTest(TestCase):
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

    def test_product_view(self):
        response = self.client.get(
            reverse('product', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store.html')


class ProductDetailViewTest(TestCase):
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

    def test_product_detail_view(self):
        response = self.client.get(
            reverse('product-detail', args=[self.category.slug, self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')


class ProductSerializerTest(TestCase):
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

    def test_product_serializer(self):
        serializer = ProductSerializer(instance=self.product)
        expected_data = {
            'id': self.product.id,
            'product_name': 'Product 1',
            'slug': 'product-1',
            'description': 'Product 1 description',
            'information': 'Product 1 information',
            'concise': 'Product 1 concise',
            'color': 'ابی',
            'size': 'XL',
            'price': '10.99',
            'stock': 100,
            'discount': 5,
            'discount_price': round(10.44, 2),  # گرد کردن به دو رقم اعشار
            'category': self.category.id
        }
        pprint.pprint(serializer.data)
        pprint.pprint(expected_data)
        self.assertEqual(serializer.data['id'], expected_data['id'])
        self.assertAlmostEqual(
            serializer.data['discount_price'], expected_data['discount_price'], places=2)
        self.assertEqual(serializer.data['product_name'],
                         expected_data['product_name'])


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title='Category 1', slug='category-1', description='Description for Category 1')

    def test_category_serializer(self):
        serializer = CategorySerializer(instance=self.category)
        expected_data = {
            'id': self.category.id,
            'title': 'Category 1',
            'slug': 'category-1',
            'description': 'Description for Category 1',
            'category_image': None,
            'parent': None,
            'children': []
        }
        self.assertEqual(serializer.data, expected_data)
        self.assertEqual(serializer.data['children'], list(
            self.category.children.all().values_list('id', flat=True)))
