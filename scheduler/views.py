from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Job
from .serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-priority', 'deadline')
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status="pending")


@login_required
def submit_job(request):
    if request.method == "POST":
        job = Job.objects.create(
            user=request.user,
            name=request.POST['name'],
            estimated_duration=int(request.POST['duration']),
            priority=request.POST['priority'],
            deadline=request.POST['deadline'],
            status="pending"
        )
        messages.success(request, "Job submitted successfully!")
        return redirect('dashboard')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')
    return render(request, "register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    jobs = Job.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'jobs': jobs})

def home(request):
    return render(request, "home.html")