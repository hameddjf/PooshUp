from django.contrib import admin


from .models import Like, UserIP


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('product', 'count', 'last_modified')


@admin.register(UserIP)
class UserIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'user', 'liked', 'timestamp')
