from django.contrib import admin
from django.utils.html import format_html

from .models import Category
# Register your models here.

# @admin.register()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('product',)
    list_display = ('title', 'category_image_tag', 'slug', 'parent')

    def category_image_tag(self, obj):
        if obj.category_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.category_image.url)
        else:
            return 'No Image'
    category_image_tag.short_description = 'Image'
