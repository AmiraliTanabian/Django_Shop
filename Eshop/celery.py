from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# به علت قطع اینترنت اعمال فرایند خودکار حذف فایل های تیکت بدون تیکت انجام نمیگردد
# پروژه ادامه پیدا میکند تا زمانی که اینترنت وصل شود
# پس از اتصال اینترنت دستورات زیر را وارد کنید:

# "Due to internet disconnection, the automated process of deleting unticketed files will not be performed.
#
# The project will continue until the internet is restored.
#
# After the internet connection is re-established, please enter the following commands:"
# sudo apt update
# sudo apt install redis-server
# sudo systemctl enable redis
# sudo systemctl start redis


# set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Eshop.settings')

app = Celery('Eshop')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.timezone = 'Asia/Tehran'
app.conf.enable_utc = False


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
