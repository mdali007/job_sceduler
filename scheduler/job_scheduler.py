import time
from datetime import datetime
# from scheduler.models import Job


def execute_jobs():
    from scheduler.models import Job  # Move import inside function

    while True:
        running_jobs = Job.objects.filter(status='running').count()
        if running_jobs < 3:
            job = Job.objects.filter(status='pending').order_by('-priority', 'deadline').first()
            if job:
                job.status = 'running'
                job.start_time = datetime.now()
                job.save()

                # Simulate job execution
                time.sleep(job.estimated_duration)

                job.status = 'completed'
                job.end_time = datetime.now()
                job.save()
        time.sleep(1)
