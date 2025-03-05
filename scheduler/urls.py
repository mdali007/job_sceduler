from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, register, user_login, user_logout, dashboard, submit_job, home

router = DefaultRouter()
router.register(r'jobs', JobViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('', home, name='home'), 
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('submit_job/', submit_job, name='submit_job'),
]
