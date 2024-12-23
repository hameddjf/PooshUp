from django.db import models

from store.models import Product
from accounts.models import Account
import json
# Create your models here.


class Like(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='likes', default=None)
    count = models.IntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True)
    device_info = models.CharField(max_length=1000, default=None)

    def get_device_info(self):
        print(f"device_info before loading: {self.device_info}")  # اضافه کنید
        try:
            if self.device_info:
                return json.loads(self.device_info)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")  # Debug information
        return {}

    def set_device_info(self, info):
        self.device_info = json.dumps(info)
        # بررسی مقداری که ذخیره می‌شود
        print(f"Setting device_info: {self.device_info}")

    def add_device(self, device_id, info):
        devices = self.get_device_info()
        if device_id not in devices:
            devices[device_id] = info
            self.set_device_info(devices)
            self.count += 1
            self.save()

    def remove_device(self, device_id):
        devices = self.get_device_info()
        if device_id in devices:
            del devices[device_id]
            self.set_device_info(devices)
            self.count = max(0, self.count - 1)  # جلوگیری از شمارنده منفی
            self.save()  # ذخیره تغییرات در model

    def has_liked(self, device_id):
        return device_id in self.get_device_info()

    # def increment(self):
    #     self.count += 1
    #     self.save()

    # def decrement(self):
    #     if self.count > 0:
    #         self.count -= 1
    #     self.save()

    class Meta:
        verbose_name = ("لایک")
        verbose_name_plural = ("لایکها")


class UserIP(models.Model):
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='liked_by', default=None)
    liked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.product.title}"

    class Meta:
        verbose_name = ("ایپی")
        verbose_name_plural = ("ایپی ها")
