from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.

class UserAdmin(UserAdmin):
    list_display = ('email' , 'first_name' , 'last_name' , 'username' , 'last_login' , 'date_joined' ,'is_active')
    list_display_links = ('email' , 'first_name' , 'username')
    readonly_fields = ('last_login' , 'date_joined')
    overdering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fielsets = ()

admin.site.register(User , UserAdmin)
# class UserAdmin(UserAdmin):
#     # fieldsets = (
#     #     (None, {'fields': ('username', 'password')}),
#     #     ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
#     #     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#     #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     # )
#     # add_fieldsets = (
#     #     (None, {
#     #         'classes': ('wide',),
#     #         'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2'),
#     #     }),
#     # )
#     list_display_links = ('email' , 'first_name' , 'username')
#     # list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'last_login' , 'date_joined' ,'is_active')
#     # readonly_fields = ('last_login' , 'date_joined')
#     search_fields = ('email', 'username', 'first_name', 'last_name')
#     ordering = ('email','-date_joined')

#     filter_horizontal = ()
#     list_filter = ()
#     fielsets = ()

# admin.site.register(User, UserAdmin)