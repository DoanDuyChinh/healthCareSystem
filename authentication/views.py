from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import User

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Redirect based on role
            if user.role == 'patient':
                return redirect('patients:create_profile')
            elif user.role == 'doctor':
                return redirect('doctors:create_profile')
            else:
                return redirect('authentication:dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'authentication/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Redirect based on role
                if user.role == 'patient':
                    return redirect('patients:dashboard')
                elif user.role == 'doctor':
                    return redirect('doctors:dashboard')
                elif user.role == 'admin':
                    return redirect('adminpanel:dashboard')
                elif user.role == 'pharmacist':
                    return redirect('pharmacy:dashboard')
                elif user.role == 'lab_technician':
                    return redirect('lab:dashboard')
                elif user.role == 'insurance_provider':
                    return redirect('billing:dashboard')
                else:
                    return redirect('authentication:dashboard')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'authentication/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('authentication:login')  # Changed from 'login' to 'authentication:login'

@login_required
def dashboard_view(request):
    return render(request, 'authentication/dashboard.html')

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'authentication/profile.html', {'user': user})
