from django.contrib import admin
from .models import Category
# Register your models here.

# @admin.register()
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title' ,)}
    list_display = ('title' , 'slug' , )

admin.site.register(Category , CategoryAdmin)