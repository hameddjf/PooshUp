from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import Account, UserProfile
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username',
                    'last_login', 'date_joined', 'is_active', 'is_admin')
    list_display_links = ('email', 'first_name', 'last_name', 'username')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
         'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name',
                       'last_name', 'is_active', 'is_admin')}
         ),
    )


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(
            '<img src="{}" width="30" style="border-radius:50%;">'.format(
                object.profile_picture.url
            )
        )
    thumbnail.short_description = 'عکس پروفایل'
    list_display = ('thumbnail', 'user', 'city', 'state')


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
