from django.contrib import admin

from .models import Product, Variation, ReviewRating, ProductGallery

import admin_thumbnails
# Register your models here.

# @admin.register()


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price', 'stock',
                    'category', 'created_date', 'is_available')
    raw_id_fields = ('category',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductGalleryInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ('variation_category',
                    'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('variation_category',
                   'variation_value')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
