import admin_thumbnails

from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Variation, ReviewRating, ProductGallery

# Register your models here.

# @admin.register()


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_image', 'price', 'discount_price', 'stock',
                    'category', 'created_date', 'is_available')
    raw_id_fields = ('category',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductGalleryInline]

    def product_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        else:
            return 'No Image'
    product_image.short_description = 'Image'


class VariationAdmin(admin.ModelAdmin):
    list_display = ('variation_category',
                    'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('variation_category',
                   'variation_value')


admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
