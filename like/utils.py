# import subprocess


# def get_windows_serial_number():
#     try:
#         # Execute the WMIC command to get the serial number
#         output = subprocess.check_output(
#             "wmic bios get serialnumber", shell=True)
#         # Decode the output to a string and split by newline
#         serial_number = output.decode().split("\n")[1].strip()
#         return serial_number
#     except Exception as e:
#         return str(e)


# print(get_windows_serial_number())
import subprocess
import uuid
import hashlib
import json


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
