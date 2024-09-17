from django.contrib import admin
from .models import Order, Payment, OrderProduct
# Register your models here.

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Payment, Order, OrderProduct


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'order__order_number')
    readonly_fields = ('created_at', 'order', 'status', 'user', 'bank_record')

    fieldsets = (
        (_('payment Information'), {
            'fields': ('order', 'bank_record', 'status')
        }),
        (_('Customer Information'), {
            'fields': ('user',)
        }),

        (_('Additional Information'), {
            'fields': ('created_at', )
        }),
    )

    # def has_add_permission(self, request):
    #     return request.user.is_superuser

    # def has_change_permission(self, request, obj=None):
    #     return request.user.is_superuser

    # def has_delete_permission(self, request, obj=None):
    #     return request.user.is_superuser


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('product', 'quantity', 'payment_status')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'phone', 'email',
                    'order_total', 'payment_status', 'is_ordered', 'created_at')
    list_filter = ('payment_status', 'is_ordered', 'created_at')
    search_fields = ('order_number', 'first_name',
                     'last_name', 'phone', 'email')
    readonly_fields = ('order_number', 'created_at',
                       'updated_at', 'payment_status',  'bank_record',  'is_ordered', 'grand_total', 'order_total', 'ip', 'tax')
    inlines = [OrderProductInline]

    fieldsets = (
        (_('Order Information'), {
            'fields': ('order_number', 'user', 'bank_record', 'payment_status', 'is_ordered')
        }),
        (_('Customer Information'), {
            'fields': ('first_name', 'last_name', 'phone', 'email')
        }),
        (_('Financial Information'), {
            'fields': ('order_total', 'tax', 'grand_total')
        }),
        (_('Additional Information'), {
            'fields': ('ip', 'created_at', 'updated_at')
        }),
    )

    # def has_add_permission(self, request):
    #     return request.user.is_superuser

    # def has_change_permission(self, request, obj=None):
    #     return request.user.is_superuser

    # def has_delete_permission(self, request, obj=None):
    #     return request.user.is_superuser


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'product', 'quantity',
                    'payment_status', 'ordered', 'created_at')
    list_filter = ('payment_status', 'ordered', 'created_at')
    search_fields = ('order__order_number', 'user__username',
                     'product__product_name')
    readonly_fields = ('quantity', 'payment_status', 'ordered',
                       'order', 'bank_record', 'created_at', 'updated_at')

    fieldsets = (
        (_('Order Information'), {
            'fields': ('order', 'bank_record', 'user', 'product', 'variation')
        }),
        (_('Order Details'), {
            'fields': ('quantity', 'payment_status', 'ordered')
        }),
        (_('Coupon'), {
            'fields': ('coupon',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )

    # def has_add_permission(self, request):
    #     return request.user.is_superuser

    # def has_change_permission(self, request, obj=None):
    #     return request.user.is_superuser

    # def has_delete_permission(self, request, obj=None):
    #     return request.user.is_superuser


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
