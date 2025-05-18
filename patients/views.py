from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import PatientProfile
from .forms import PatientProfileForm
from appointments.models import Appointment
from doctors.models import MedicalRecord, Prescription

@login_required
def create_profile_view(request):
    if request.user.role != 'patient':
        messages.error(request, "Only patients can create patient profiles.")
        return redirect('authentication:dashboard')
    
    try:
        # Check if profile already exists
        profile = PatientProfile.objects.get(user=request.user)
        messages.info(request, "You already have a profile.")
        return redirect('patients:dashboard')
    except PatientProfile.DoesNotExist:
        if request.method == 'POST':
            form = PatientProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, "Your profile has been created successfully!")
                return redirect('patients:dashboard')
        else:
            form = PatientProfileForm()
            
        return render(request, 'patients/create_profile.html', {'form': form})

@login_required
def dashboard_view(request):
    if request.user.role != 'patient':
        messages.error(request, "Access denied. You are not registered as a patient.")
        return redirect('authentication:dashboard')
    
    try:
        profile = PatientProfile.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patient=profile).order_by('-date')
        medical_records = MedicalRecord.objects.filter(patient=profile).order_by('-date')
        
        # Pagination for appointments
        appointment_paginator = Paginator(appointments, 5)
        appointment_page = request.GET.get('appointment_page')
        appointments_page_obj = appointment_paginator.get_page(appointment_page)
        
        # Pagination for medical records
        record_paginator = Paginator(medical_records, 5)
        record_page = request.GET.get('record_page')
        records_page_obj = record_paginator.get_page(record_page)
        
        context = {
            'profile': profile,
            'appointments': appointments_page_obj,
            'medical_records': records_page_obj,
        }
        
        return render(request, 'patients/dashboard.html', context)
    except PatientProfile.DoesNotExist:
        messages.warning(request, "Please complete your profile first.")
        return redirect('patients:create_profile')

@login_required
def edit_profile_view(request):
    if request.user.role != 'patient':
        messages.error(request, "Access denied. You are not registered as a patient.")
        return redirect('authentication:dashboard')
    
    profile = get_object_or_404(PatientProfile, user=request.user)
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('patients:dashboard')
    else:
        form = PatientProfileForm(instance=profile)
    
    return render(request, 'patients/edit_profile.html', {'form': form})

@login_required
def medical_record_detail_view(request, record_id):
    if request.user.role != 'patient':
        messages.error(request, "Access denied. You are not registered as a patient.")
        return redirect('authentication:dashboard')
    
    profile = get_object_or_404(PatientProfile, user=request.user)
    record = get_object_or_404(MedicalRecord, id=record_id, patient=profile)
    prescriptions = Prescription.objects.filter(record=record)
    
    context = {
        'record': record,
        'prescriptions': prescriptions,
    }
    
    return render(request, 'patients/medical_record_detail.html', context)
