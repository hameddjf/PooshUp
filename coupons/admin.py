from django.contrib import admin
from .models import Coupon
# Register your models here.


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'discount_percent',
        'coupon_type',
        'coupon_validity_time',
        'used_count',
        'maximum_uses',
        'is_active',
        'created_date',
        'updated_date',
        'is_valid',  # تاکیدی بر اینکه اینجا اضافه شده است
    )

    search_fields = ('code',)
    list_filter = ('coupon_type', 'is_active', 'coupon_validity_time')
    ordering = ('-created_date',)

    fieldsets = (
        (None, {'fields': ('code', 'discount_percent', 'coupon_type')}),
        (None, {'fields': ('coupon_validity_time',
         'maximum_uses', 'used_count', 'is_active')}),
    )

    def is_valid(self, obj):
        # فضای ساده‌تری برای پاسخ‌دهی، چون شما نیازی به order_status ندارید.
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Valid'
