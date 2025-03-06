from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, user_jobs, register, user_login, user_logout, index, submit_job

router = DefaultRouter()
router.register(r'jobs', JobViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('api/', include(router.urls)),
    path('api/my-jobs/', user_jobs, name='user_jobs'),
    path('submit_job/', submit_job, name='submit_job'),
]
