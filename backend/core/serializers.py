from rest_framework import serializers
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_discount_price(self, obj):
        return obj.discount_price


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Category
        fields = '__all__'
