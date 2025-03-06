from django.apps import AppConfig

class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        import threading
        from django.db import connections
        if not connections.databases:  # Ensure the database is available
            return

        from .job_scheduler import execute_jobs  # Move import inside the function
        threading.Thread(target=execute_jobs, daemon=True).start()
