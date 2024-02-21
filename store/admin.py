from django.contrib import admin
from .models import Product
# Register your models here.

# @admin.register()


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price', 'stock',
                    'category', 'created_date', 'is_available')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Product, ProductAdmin)
