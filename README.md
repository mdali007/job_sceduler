# job_sceduler

A Django-based Job Scheduling System that manages priority-based job execution with REST APIs and authentication.

## Project Features

-  User Authentication (Buildin Django authentication) – Register, Login, Logout
-  Job Management (Django REST Framework)
-  Custom Job Scheduling Algorithm
-  Simulated Job Execution – Uses `time.sleep()` to represent work
-  Job Dashboard – Displays submtted jobs and execution status

## Technologies Used

- Backend: Django, Django REST Framework (DRF)
- Database: (SQLite by default can change in prodction tym to PostgreSQL by updating it in settings.py)
- Frontend: HTML, Bootstrap, jQuery (AJAX for API calls)
- Task Execution: Python Threading

# Setup Instructions

- 1. Clone the Repository
     git clone 

- 2. Create a Virtual Environment and activate

- 3. Install Dependencies

- 4. Apply Migrations & Setup Database

- 5. Create a Superuser 

- 6. Run the Server


#  Database Schema

Job Model (`scheduler/models.py`)

from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    estimated_duration = models.IntegerField()  # in seconds
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
