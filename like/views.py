from django.views.generic import View
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import get_object_or_404

from datetime import timedelta
import subprocess
import uuid
import hashlib
import json
from .models import Like, UserIP
from .utils import get_device_id


from store.models import Product
from accounts.models import Account


class LikeItemView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        device_id = self.get_device_id(request)

        # جستجوی وجود لایک برای این محصول و دستگاه
        like, created = Like.objects.get_or_create(
            product=product, device_info=device_id, defaults={'count': 1})

        if like:  # اگر لایک وجود دارد
            like.remove_device(device_id)
            action = 'unlike'
        else:  # اگر لایک وجود ندارد
            like = Like(product=product, device_info=device_id)
            # افزودن اطلاعات دستگاه
            # اینجا نیاز است که شما اطلاعات دستگاه را بگیرید.
            device_info = self.get_device_info(request)
            like.set_device_info(json.dumps(device_info))
            like.count == 1  # از 1 شروع می‌شود زیرا این اولین لایک است
            like.save()
            action = 'like'
        like.save()
        referer = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(referer)

    def get_device_id(self, request):
        # دریافت شناسه دستگاه
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip = request.META.get('REMOTE_ADDR', '')

        # تشخیص سیستم‌عامل و نوع دستگاه
        device_type = ''
        serial_number = ''

        if 'Windows' in user_agent:
            device_type = 'Windows'
            try:
                output = subprocess.check_output(
                    "wmic bios get serialnumber", shell=True)
                serial_number = output.decode().split("\n")[1].strip()
            except Exception:
                serial_number = ''
        elif 'Macintosh' in user_agent:
            device_type = 'Mac'
            # در اینجا می‌توانید برای Mac کارهای دیگری انجام دهید (شناسایی سریال یا دیگر اطلاعات)
        elif 'Linux' in user_agent:
            device_type = 'Linux'
            # اطلاعات مربوط به Linux
        elif 'iPhone' in user_agent or 'iPad' in user_agent:
            device_type = 'iOS'
            # اطلاعات مربوط به دستگاه‌های iOS
        elif 'Android' in user_agent:
            device_type = 'Android'
            # اطلاعات مربوط به دستگاه‌های Android

        device_info = f"{device_type}{user_agent}{ip}{serial_number}"
        device_id = hashlib.md5(device_info.encode()).hexdigest()

        return device_id

    def get_device_info(self, request):
        # اطلاعات دستگاه را از درخواست دریافت کنید
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip = request.META.get('REMOTE_ADDR', '')

        return {
            "user_agent": user_agent,
            "ip": ip
            # اطلاعات دیگری که برای شما مهم است می‌توانید اضافه کنید
        }
