from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from django.utils import timezone  # Add this import
from .models import DoctorProfile, MedicalRecord, Prescription
from .forms import DoctorProfileForm, MedicalRecordForm, PrescriptionForm
from patients.models import PatientProfile
from appointments.models import Appointment

@login_required
def create_profile_view(request):
    if request.user.role != 'doctor':
        messages.error(request, "Only doctors can create doctor profiles.")
        return redirect('authentication:dashboard')
    
    try:
        # Check if profile already exists
        profile = DoctorProfile.objects.get(user=request.user)
        messages.info(request, "You already have a profile.")
        return redirect('doctors:dashboard')
    except DoctorProfile.DoesNotExist:
        if request.method == 'POST':
            form = DoctorProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, "Your profile has been created successfully!")
                return redirect('doctors:dashboard')
        else:
            form = DoctorProfileForm()
            
        return render(request, 'doctors/create_profile.html', {'form': form})

@login_required
def dashboard_view(request):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied. You are not registered as a doctor.")
        return redirect('authentication:dashboard')
    
    try:
        profile = DoctorProfile.objects.get(user=request.user)
        
        # Use a safer query that doesn't rely on the completed_at field
        try:
            upcoming_appointments = Appointment.objects.filter(
                doctor=profile, 
                status='approved',
                date__gt=timezone.now()
            ).order_by('date')[:5]
        except Exception as e:
            # Fallback if there's a database issue
            upcoming_appointments = []
            messages.warning(request, "Unable to load appointments due to a database issue. Please try again later.")
        
        # Recent records don't depend on the appointment completed_at field
        recent_records = MedicalRecord.objects.filter(
            doctor=profile
        ).order_by('-date')[:5]
        
        context = {
            'profile': profile,
            'upcoming_appointments': upcoming_appointments,
            'recent_records': recent_records,
        }
        
        return render(request, 'doctors/dashboard.html', context)
    except DoctorProfile.DoesNotExist:
        messages.warning(request, "Please complete your profile first.")
        return redirect('doctors:create_profile')

@login_required
def edit_profile_view(request):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied. You are not registered as a doctor.")
        return redirect('authentication:dashboard')
    
    profile = get_object_or_404(DoctorProfile, user=request.user)
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('doctors:dashboard')
    else:
        form = DoctorProfileForm(instance=profile)
    
    return render(request, 'doctors/edit_profile.html', {'form': form})

@login_required
def patient_list_view(request):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied. You are not registered as a doctor.")
        return redirect('authentication:dashboard')
    
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    
    # Get unique patients who have had appointments with this doctor
    # Add ordering to prevent UnorderedObjectListWarning
    patients = PatientProfile.objects.filter(
        medical_records__doctor=doctor
    ).distinct().order_by('user__last_name', 'user__first_name')
    
    paginator = Paginator(patients, 10)
    page = request.GET.get('page')
    patients_page = paginator.get_page(page)
    
    return render(request, 'doctors/patient_list.html', {'patients': patients_page})

@login_required
def create_medical_record_view(request, patient_id):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied. You are not registered as a doctor.")
        return redirect('authentication:dashboard')
    
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    patient = get_object_or_404(PatientProfile, id=patient_id)
    
    PrescriptionFormSet = inlineformset_factory(
        MedicalRecord, Prescription, 
        form=PrescriptionForm, 
        extra=1, can_delete=False
    )
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        formset = PrescriptionFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            record = form.save(commit=False)
            record.doctor = doctor
            record.patient = patient
            record.save()
            
            prescriptions = formset.save(commit=False)
            for prescription in prescriptions:
                prescription.record = record
                prescription.save()
            
            messages.success(request, "Medical record created successfully.")
            return redirect('doctors:patient_detail', patient_id=patient.id)
    else:
        form = MedicalRecordForm()
        formset = PrescriptionFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'patient': patient,
    }
    
    return render(request, 'doctors/create_medical_record.html', context)

@login_required
def patient_detail_view(request, patient_id):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied. You are not registered as a doctor.")
        return redirect('authentication:dashboard')
    
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    patient = get_object_or_404(PatientProfile, id=patient_id)
    
    medical_records = MedicalRecord.objects.filter(
        doctor=doctor,
        patient=patient
    ).order_by('-date')
    
    appointments = Appointment.objects.filter(
        doctor=doctor,
        patient=patient
    ).order_by('-date')
    
    # Get lab tests for this patient ordered by this doctor
    from lab.models import LabTest
    lab_tests = LabTest.objects.filter(
        doctor=doctor,
        patient=patient
    ).order_by('-ordered_at')
    
    context = {
        'patient': patient,
        'medical_records': medical_records,
        'appointments': appointments,
        'lab_tests': lab_tests,  # Add lab tests to the context
    }
    
    return render(request, 'doctors/patient_detail.html', context)

@login_required
def record_detail_view(request, record_id):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied. You are not registered as a doctor.")
        return redirect('authentication:dashboard')
    
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    record = get_object_or_404(MedicalRecord, id=record_id, doctor=doctor)
    prescriptions = Prescription.objects.filter(record=record)
    
    context = {
        'record': record,
        'prescriptions': prescriptions,
    }
    
    return render(request, 'doctors/record_detail.html', context)

@login_required
def add_prescription_view(request, record_id):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied. You are not registered as a doctor.")
        return redirect('authentication:dashboard')
    
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    record = get_object_or_404(MedicalRecord, id=record_id, doctor=doctor)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.record = record
            prescription.save()
            messages.success(request, "Prescription added successfully.")
            return redirect('doctors:record_detail', record_id=record.id)
    else:
        form = PrescriptionForm()
    
    context = {
        'form': form,
        'record': record,
    }
    
    return render(request, 'doctors/add_prescription.html', context)
