from django.contrib import admin
from .models import ContactPage


@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'title', 'created_at')
    search_fields = ('name', 'email', 'title')
    list_filter = ('created_at',)


# @admin.register(AboutPage)
# class AboutPageAdmin(admin.ModelAdmin):
#     list_display = ('title', 'image')
#     search_fields = ('title',)
#     # Optional: Prepopulate if needed
#     prepopulated_fields = {'title': ('content',)}
