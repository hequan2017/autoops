from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoops.settings')
# celery 5 移除了 celery.platforms，允许 root 运行改用环境变量
os.environ.setdefault('C_FORCE_ROOT', 'true')

app = Celery('autoops')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
