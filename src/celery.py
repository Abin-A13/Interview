import os
from celery import celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE","src.settings")

app = celery('task_app')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()