from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .models import LabTest
from .forms import OrderLabTestForm, UpdateLabTestForm
from patients.models import PatientProfile
from doctors.models import DoctorProfile

@login_required
def order_test_view(request, patient_id):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied. Only doctors can order lab tests.")
        return redirect('authentication:dashboard')
    
    try:
        doctor = DoctorProfile.objects.get(user=request.user)
        patient = get_object_or_404(PatientProfile, id=patient_id)
        
        if request.method == 'POST':
            form = OrderLabTestForm(request.POST)
            if form.is_valid():
                test = form.save(commit=False)
                test.doctor = doctor
                test.patient = patient
                test.save()
                
                messages.success(request, "Lab test ordered successfully.")
                return redirect('doctors:patient_detail', patient_id=patient.id)
        else:
            form = OrderLabTestForm()
        
        context = {
            'form': form,
            'patient': patient,
        }
        
        return render(request, 'lab/order_test.html', context)
        
    except DoctorProfile.DoesNotExist:
        messages.warning(request, "Doctor profile not found.")
        return redirect('doctors:create_profile')

@login_required
def update_test_view(request, test_id):
    if request.user.role != 'lab_technician':
        messages.error(request, "Access denied. Only lab technicians can update test results.")
        return redirect('authentication:dashboard')
    
    test = get_object_or_404(LabTest, id=test_id)
    
    if request.method == 'POST':
        form = UpdateLabTestForm(request.POST, request.FILES, instance=test)
        if form.is_valid():
            lab_test = form.save()
            
            if lab_test.status == 'completed' and not lab_test.completed_at:
                lab_test.completed_at = timezone.now()
                lab_test.save()
                
            messages.success(request, "Lab test updated successfully.")
            return redirect('lab:dashboard')
    else:
        form = UpdateLabTestForm(instance=test)
    
    context = {
        'form': form,
        'test': test,
    }
    
    return render(request, 'lab/update_test.html', context)

@login_required
def dashboard_view(request):
    if request.user.role != 'lab_technician':
        messages.error(request, "Access denied. Only lab technicians can access the lab dashboard.")
        return redirect('authentication:dashboard')
    
    # Get tests that are not yet completed
    pending_tests = LabTest.objects.filter(
        status__in=['ordered', 'sample_collected', 'processing']
    ).order_by('ordered_at')
    
    # Get completed tests
    completed_tests = LabTest.objects.filter(
        status='completed'
    ).order_by('-completed_at')
    
    # Pagination
    pending_paginator = Paginator(pending_tests, 10)
    pending_page = request.GET.get('pending_page')
    pending_page_obj = pending_paginator.get_page(pending_page)
    
    completed_paginator = Paginator(completed_tests, 10)
    completed_page = request.GET.get('completed_page')
    completed_page_obj = completed_paginator.get_page(completed_page)
    
    context = {
        'pending_tests': pending_page_obj,
        'completed_tests': completed_page_obj,
    }
    
    return render(request, 'lab/dashboard.html', context)

@login_required
def test_detail_view(request, test_id):
    if request.user.role not in ['doctor', 'lab_technician', 'patient']:
        messages.error(request, "Access denied.")
        return redirect('authentication:dashboard')
    
    test = get_object_or_404(LabTest, id=test_id)
    
    # Check permissions
    if request.user.role == 'doctor' and test.doctor.user != request.user:
        messages.error(request, "Access denied. You are not the ordering doctor.")
        return redirect('authentication:dashboard')
    
    if request.user.role == 'patient' and test.patient.user != request.user:
        messages.error(request, "Access denied. This test is not yours.")
        return redirect('authentication:dashboard')
    
    context = {
        'test': test,
    }
    
    return render(request, 'lab/test_detail.html', context)

@login_required
def patient_tests_view(request):
    if request.user.role != 'patient':
        messages.error(request, "Access denied.")
        return redirect('authentication:dashboard')
    
    try:
        patient = PatientProfile.objects.get(user=request.user)
        tests = LabTest.objects.filter(patient=patient).order_by('-ordered_at')
        
        paginator = Paginator(tests, 10)
        page = request.GET.get('page')
        tests_page = paginator.get_page(page)
        
        context = {
            'tests': tests_page,
        }
        
        return render(request, 'lab/patient_tests.html', context)
        
    except PatientProfile.DoesNotExist:
        messages.warning(request, "Patient profile not found.")
        return redirect('patients:create_profile')
