from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import Job
from .serializers import JobSerializer

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
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, "index.html")


def user_logout(request):
    logout(request)
    return redirect('index')

# @login_required
# def dashboard(request):
#     jobs = Job.objects.filter(user=request.user)
#     return render(request, 'dashboard.html', {'jobs': jobs})


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-priority', 'deadline')
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
       try:
        serializer.save(user=self.request.user)
       except Exception as e:
        print("ERROR:", str(e)) 
        raise e


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_jobs(request):
    jobs = Job.objects.filter(user=request.user)
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)

def index(request):
    return render(request, 'index.html')



@csrf_exempt  # Temporarily disable CSRF for testing (remove later)
def submit_job(request):
    if request.method == "POST":
        print("Raw Request Data:", request.POST.dict())  # Debugging: Print received data

        name = request.POST.get('name')
        duration = request.POST.get('estimated_duration')
        priority = request.POST.get('priority')
        deadline = request.POST.get('deadline')

        if not (name and duration and priority and deadline):
            print(f"Missing data: {name}, {duration}, {priority}, {deadline}")  # Debugging
            return JsonResponse({"error": "All fields are required."}, status=400)

        try:
            job = Job.objects.create(
                user=request.user,
                name=name,
                estimated_duration=int(duration),
                priority=priority,
                deadline=datetime.fromisoformat(deadline),  # Ensure proper datetime format
                status="pending"
            )
            return JsonResponse({"message": "Job submitted successfully!"}, status=201)
        except Exception as e:
            print(f"Error creating job: {str(e)}")  # Debugging
            return JsonResponse({"error": "Error creating job."}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)