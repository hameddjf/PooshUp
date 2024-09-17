from django import template

from .models import Coupon


register = template.Library()


class OrderProductPriceCalculator:
    def __init__(self, order_product):
        self.order_product = order_product

    @property
    def total_price_with_discount(self):
        return self.order_product.product.discount_price * self.order_product.quantity

    @property
    def total_price_with_coupon(self):
        return self.calc_price_with_coupon()

    def calc_price_with_coupon(self):
        total_price_with_discount = self.total_price_with_discount
        if self.order_product.coupon:
            discount_amount = self.order_product.coupon.calculate_discount_amount(
                total_price_with_discount)
            total_price_with_coupon = total_price_with_discount - discount_amount
        else:
            total_price_with_coupon = total_price_with_discount
        return total_price_with_coupon

    def apply_coupon(self, coupon, total_price_with_discount):
        if coupon.is_valid(order_status='OnPay'):
            discount_amount = coupon.calculate_discount_amount(
                total_price_with_discount)
            return total_price_with_discount - discount_amount
        else:
            return total_price_with_discount
