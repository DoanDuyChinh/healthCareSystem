from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from authentication.models import User
from patients.models import PatientProfile
from doctors.models import DoctorProfile, MedicalRecord
from appointments.models import Appointment
from pharmacy.models import Medicine, MedicineDispense
from lab.models import LabTest
from billing.models import Bill, Payment
from django.core.paginator import Paginator

@login_required
def dashboard_view(request):
    if request.user.role != 'admin':
        messages.error(request, "Access denied. Only administrators can access this page.")
        return redirect('authentication:dashboard')
    
    # Today's date range
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    today_end = timezone.make_aware(timezone.datetime.combine(tomorrow, timezone.datetime.min.time()))
    
    # Get counts for dashboard
    total_patients = PatientProfile.objects.count()
    total_doctors = DoctorProfile.objects.count()
    total_appointments = Appointment.objects.count()
    today_appointments = Appointment.objects.filter(date__range=(today_start, today_end)).count()
    
    # Get counts for various statuses
    pending_appointments = Appointment.objects.filter(status='pending').count()
    approved_appointments = Appointment.objects.filter(status='approved').count()
    
    # Get financial data
    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    unpaid_bills = Bill.objects.filter(status='unpaid').count()
    
    # Get latest appointments
    latest_appointments = Appointment.objects.all().order_by('-date')[:5]
    
    # Get medicine stock alerts
    low_stock_medicines = Medicine.objects.filter(stock_quantity__lt=10).order_by('stock_quantity')
    
    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'today_appointments': today_appointments,
        'pending_appointments': pending_appointments,
        'approved_appointments': approved_appointments,
        'total_revenue': total_revenue,
        'unpaid_bills': unpaid_bills,
        'latest_appointments': latest_appointments,
        'low_stock_medicines': low_stock_medicines,
    }
    
    return render(request, 'adminpanel/dashboard.html', context)

@login_required
def user_management_view(request):
    if request.user.role != 'admin':
        messages.error(request, "Access denied. Only administrators can access this page.")
        return redirect('authentication:dashboard')
    
    # Get filter parameters
    role_filter = request.GET.get('role', '')
    search_query = request.GET.get('search', '')
    
    # Start with all users
    users_query = User.objects.all()
    
    # Apply role filter if provided
    if role_filter:
        users_query = users_query.filter(role=role_filter)
    
    # Apply search filter if provided
    if search_query:
        users_query = users_query.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Order results
    users = users_query.order_by('username')
    
    # Paginate results
    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    users_page = paginator.get_page(page)
    
    context = {
        'users': users_page,
        'role_filter': role_filter,
        'search_query': search_query,
    }
    
    return render(request, 'adminpanel/user_management.html', context)

@login_required
def report_view(request):
    if request.user.role != 'admin':
        messages.error(request, "Access denied. Only administrators can access this page.")
        return redirect('authentication:dashboard')
    
    # Get date range from request or use default (last 30 days)
    now = timezone.now()
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')
    
    try:
        if start_date_str:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d')
            start_date = timezone.make_aware(start_date)
        else:
            start_date = now - timedelta(days=30)
            
        if end_date_str:
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d')
            end_date = timezone.make_aware(timezone.datetime.combine(end_date, timezone.datetime.max.time()))
        else:
            end_date = now
    except ValueError:
        start_date = now - timedelta(days=30)
        end_date = now
        messages.error(request, "Invalid date format. Using default date range.")
    
    # Generate reports based on date range
    appointments_by_day = Appointment.objects.filter(
        date__range=(start_date, end_date)
    ).extra({'date': "date(date)"}).values('date').annotate(count=Count('id')).order_by('date')
    
    revenue_by_day = Payment.objects.filter(
        payment_date__range=(start_date, end_date)
    ).extra({'date': "date(payment_date)"}).values('date').annotate(total=Sum('amount')).order_by('date')
    
    # Most active doctors
    active_doctors = Appointment.objects.filter(
        date__range=(start_date, end_date)
    ).values('doctor__user__first_name', 'doctor__user__last_name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Appointment statuses
    appointment_statuses = Appointment.objects.filter(
        date__range=(start_date, end_date)
    ).values('status').annotate(count=Count('id'))
    
    context = {
        'start_date': start_date.date(),
        'end_date': end_date.date(),
        'appointments_by_day': appointments_by_day,
        'revenue_by_day': revenue_by_day,
        'active_doctors': active_doctors,
        'appointment_statuses': appointment_statuses,
    }
    
    return render(request, 'adminpanel/reports.html', context)

@login_required
def system_settings_view(request):
    if request.user.role != 'admin':
        messages.error(request, "Access denied. Only administrators can access this page.")
        return redirect('authentication:dashboard')
    
    # This would typically include system-wide settings
    # For now, just display a placeholder page
    return render(request, 'adminpanel/system_settings.html')
