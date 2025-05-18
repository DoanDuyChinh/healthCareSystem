from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Appointment
from .forms import AppointmentForm, AppointmentStatusForm
from patients.models import PatientProfile
from doctors.models import DoctorProfile

@login_required
def book_appointment_view(request):
    if request.user.role != 'patient':
        messages.error(request, "Only patients can book appointments.")
        return redirect('authentication:dashboard')
    
    try:
        patient = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        messages.warning(request, "Please complete your profile before booking an appointment.")
        return redirect('patients:create_profile')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            
            messages.success(request, "Your appointment has been booked successfully and is pending approval.")
            return redirect('appointments:my_appointments')
    else:
        form = AppointmentForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'appointments/book_appointment.html', context)

@login_required
def my_appointments_view(request):
    if request.user.role != 'patient':
        messages.error(request, "Access denied.")
        return redirect('authentication:dashboard')
    
    try:
        patient = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        messages.warning(request, "Please complete your profile first.")
        return redirect('patients:create_profile')
    
    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        date__gt=timezone.now()
    ).order_by('date')
    
    past_appointments = Appointment.objects.filter(
        patient=patient,
        date__lte=timezone.now()
    ).order_by('-date')
    
    # Pagination
    upcoming_paginator = Paginator(upcoming_appointments, 5)
    upcoming_page = request.GET.get('upcoming_page')
    upcoming_page_obj = upcoming_paginator.get_page(upcoming_page)
    
    past_paginator = Paginator(past_appointments, 5)
    past_page = request.GET.get('past_page')
    past_page_obj = past_paginator.get_page(past_page)
    
    context = {
        'upcoming_appointments': upcoming_page_obj,
        'past_appointments': past_page_obj,
    }
    
    return render(request, 'appointments/my_appointments.html', context)

@login_required
def cancel_appointment_view(request, appointment_id):
    if request.user.role != 'patient':
        messages.error(request, "Access denied.")
        return redirect('authentication:dashboard')
    
    try:
        patient = PatientProfile.objects.get(user=request.user)
        appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)
        
        if appointment.is_past_due():
            messages.error(request, "Cannot cancel a past appointment.")
            return redirect('appointments:my_appointments')
        
        if appointment.status == 'cancelled':
            messages.info(request, "This appointment is already cancelled.")
            return redirect('appointments:my_appointments')
        
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, "Appointment cancelled successfully.")
        
    except PatientProfile.DoesNotExist:
        messages.warning(request, "Patient profile not found.")
    
    return redirect('appointments:my_appointments')

@login_required
def doctor_appointments_view(request):
    # Allow both doctors and admins to access this view
    if request.user.role not in ['doctor', 'admin']:
        messages.error(request, "Access denied. Only doctors and administrators can access this page.")
        return redirect('authentication:dashboard')
    
    # Handle differently based on user role
    if request.user.role == 'doctor':
        try:
            doctor = DoctorProfile.objects.get(user=request.user)
        except DoctorProfile.DoesNotExist:
            messages.warning(request, "Please complete your profile first.")
            return redirect('doctors:create_profile')
            
        # Get all appointment types for this specific doctor
        upcoming_appointments = Appointment.objects.filter(
            doctor=doctor,
            date__gt=timezone.now()
        ).order_by('date')
    else:  # Admin can see all appointments
        # Get all appointment types for all doctors
        upcoming_appointments = Appointment.objects.filter(
            date__gt=timezone.now()
        ).order_by('date')
        
        # For admin, we don't need a doctor profile
        doctor = None
    
    # Filter appointments by status
    pending_appointments = upcoming_appointments.filter(status='pending')
    approved_appointments = upcoming_appointments.filter(status='approved')
    
    # Get all past appointments, including completed ones
    if request.user.role == 'doctor':
        past_appointments = Appointment.objects.filter(
            doctor=doctor,
            date__lte=timezone.now()
        ).order_by('-date')
    else:  # Admin
        past_appointments = Appointment.objects.filter(
            date__lte=timezone.now()
        ).order_by('-date')
    
    # Paginate past appointments
    past_paginator = Paginator(past_appointments, 10)
    past_page = request.GET.get('past_page')
    past_page_obj = past_paginator.get_page(past_page)
    
    context = {
        'pending_appointments': pending_appointments,
        'approved_appointments': approved_appointments,
        'past_appointments': past_page_obj,  # Use paginated version
    }
    
    return render(request, 'appointments/doctor_appointments.html', context)

@login_required
def update_appointment_status_view(request, appointment_id):
    if request.user.role != 'doctor':
        messages.error(request, "Access denied. Only doctors can update appointment status.")
        return redirect('authentication:dashboard')
    
    try:
        doctor = DoctorProfile.objects.get(user=request.user)
        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
        
        if request.method == 'POST':
            previous_status = appointment.status
            form = AppointmentStatusForm(request.POST, instance=appointment)
            if form.is_valid():
                updated_appointment = form.save()
                
                # If status is changed to completed, perform additional actions
                if updated_appointment.status == 'completed' and previous_status != 'completed':
                    # Create a billing record for this appointment
                    from billing.models import Bill
                    
                    # Create bill for this appointment if it doesn't exist
                    if not hasattr(appointment, 'bill'):
                        bill = Bill.objects.create(
                            patient=appointment.patient,
                            bill_type='appointment',
                            appointment=appointment,
                            amount=appointment.doctor.consulting_fee,
                            description=f"Consultation with Dr. {appointment.doctor.user.get_full_name()} on {appointment.date.strftime('%Y-%m-%d %H:%M')}",
                            due_date=timezone.now() + timezone.timedelta(days=30)
                        )
                        messages.info(request, f"Bill #{bill.id} has been generated for this appointment.")
                
                messages.success(request, "Appointment status updated successfully.")
                
                # If completed, redirect to create medical record
                if updated_appointment.status == 'completed':
                    messages.info(request, "Please create a medical record for this appointment.")
                    return redirect('doctors:create_record', patient_id=appointment.patient.id)
                
                return redirect('appointments:doctor_appointments')
        else:
            form = AppointmentStatusForm(instance=appointment)
        
        context = {
            'form': form,
            'appointment': appointment,
        }
        
        return render(request, 'appointments/update_status.html', context)
        
    except DoctorProfile.DoesNotExist:
        messages.warning(request, "Doctor profile not found.")
        return redirect('doctors:create_profile')
