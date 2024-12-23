import logging
from azbankgateways.models import Bank

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from .models import Order, OrderProduct, Payment

from store.models import Product, Variation
from coupons.models import Coupon
from carts.models import CartItem


@receiver(post_save, sender=Bank)
def create_or_update_payment_on_bank_record_change(sender, instance, created, **kwargs):
    logging.info(f"Bank record {
                 'created' if created else 'updated'}: {instance.id}")
    try:
        order = Order.objects.get(bank_record=instance)
        payment, created = Payment.objects.get_or_create(
            bank_record=instance,
            defaults={
                'user': order.user,
                'order': order,
                'status': 'pending'
            }
        )
        if not created:
            # Update existing payment
            payment.status = 'completed' if instance.is_success else 'failed'
            payment.save()

        logging.info(
            f"Payment {'created' if created else 'updated'} for order {order.id}")

    except Order.DoesNotExist:
        logging.error(f"Order not found for bank record {
                      instance.tracking_code}")
    except Exception as e:
        logging.error(
            f"Error in create_or_update_payment_on_bank_record_change: {str(e)}")


@receiver(post_save, sender=Payment)
def update_order_status(sender, instance, created, **kwargs):
    if not created and instance.status == 'completed':
        try:
            with transaction.atomic():
                order = Order.objects.get(id=instance.order_id)
                order.is_ordered = True
                order.payment_status = 'completed'
                order.save()
                logging.info(
                    f"Order {order.id} updated based on Payment {instance.id}")
        except Order.DoesNotExist:
            logging.error(f"Order not found for Payment {instance.id}")
        except Exception as e:
            logging.error(f"Error in update_order_status: {str(e)}")


@receiver(post_save, sender=Order)
def create_order_products(sender, instance, **kwargs):
    if instance.is_ordered and instance.payment_status == 'completed' and instance.bank_record:
        try:
            with transaction.atomic():
                if not OrderProduct.objects.filter(order=instance).exists():
                    cart_items = instance.user.cartitem_set.all()
                    for item in cart_items:
                        order_product = OrderProduct.objects.create(
                            order=instance,
                            user=instance.user,
                            product=item.product,
                            quantity=item.quantity,
                            payment_status="completed",
                            ordered=True,
                            coupon=item.coupon,
                            bank_record=instance.bank_record  # اضافه کردن رکورد بانکی
                        )

                        variations = item.variations.all()
                        order_product.variation.set(variations)

                        # # کاهش موجودی محصول
                        product = item.product
                        if product.stock >= item.quantity:
                            product.stock -= item.quantity
                            product.save()
                        else:
                            raise ValueError(
                                f"Insufficient stock for product {product.id}")

                        if item.coupon:
                            pass

                    # پاک کردن سبد خرید کاربر
                    cart_items.delete()
                    logging.info(
                        f"OrderProducts created for Order {instance.id} with bank record {instance.bank_record.id}")
                else:
                    logging.info(
                        f"OrderProducts already exist for Order {instance.id}")
        except Exception as e:
            logging.error(f"Error in create_order_products: {str(e)}")
    else:
        logging.info(
            f"Order {instance.id} is not ready for creating OrderProducts")
