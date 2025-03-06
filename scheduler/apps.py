from django.apps import AppConfig

class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        import threading
        from django.db import connections
        if not connections.databases:  
            return

        from .job_scheduler import execute_jobs 
        threading.Thread(target=execute_jobs, daemon=True).start()
