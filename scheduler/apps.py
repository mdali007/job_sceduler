from django.apps import AppConfig
import threading
from .job_scheduler import execute_jobs


class SchedulerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "scheduler"

    def ready(self):
        threading.Thread(target=execute_jobs, daemon=True).start()