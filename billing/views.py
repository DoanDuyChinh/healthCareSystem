from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Sum, Q
from .models import Bill, Payment, InsuranceClaim
from .forms import BillForm, PaymentForm, InsuranceClaimForm, InsuranceClaimUpdateForm
from patients.models import PatientProfile
from appointments.models import Appointment
from pharmacy.models import MedicineDispense
from lab.models import LabTest

@login_required
def dashboard_view(request):
    if request.user.role not in ['admin', 'insurance_provider']:
        messages.error(request, "Access denied.")
        return redirect('authentication:dashboard')
    
    # Get stats for admin/insurance provider dashboard
    total_bills = Bill.objects.count()
    total_unpaid = Bill.objects.filter(status='unpaid').count()
    total_overdue = Bill.objects.filter(
        status__in=['unpaid', 'partially_paid'],
        due_date__lt=timezone.now()
    ).count()
    
    # Get total revenue
    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    # Get pending insurance claims
    pending_claims = InsuranceClaim.objects.filter(
        status__in=['submitted', 'in_progress']
    ).order_by('submitted_at')
    
    context = {
        'total_bills': total_bills,
        'total_unpaid': total_unpaid,
        'total_overdue': total_overdue,
        'total_revenue': total_revenue,
        'pending_claims': pending_claims,
    }
    
    return render(request, 'billing/dashboard.html', context)

@login_required
def generate_bill_view(request):
    if request.user.role != 'admin':
        messages.error(request, "Access denied. Only admins can generate bills.")
        return redirect('authentication:dashboard')
    
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bill generated successfully.")
            return redirect('billing:bill_list')
    else:
        form = BillForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'billing/generate_bill.html', context)

@login_required
def bill_list_view(request):
    if request.user.role == 'admin':
        bills = Bill.objects.all().order_by('-created_at')
    elif request.user.role == 'patient':
        try:
            patient = PatientProfile.objects.get(user=request.user)
            bills = Bill.objects.filter(patient=patient).order_by('-created_at')
        except PatientProfile.DoesNotExist:
            messages.warning(request, "Patient profile not found.")
            return redirect('patients:create_profile')
    else:
        messages.error(request, "Access denied.")
        return redirect('authentication:dashboard')
    
    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        bills = bills.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(bills, 10)
    page = request.GET.get('page')
    bills_page = paginator.get_page(page)
    
    context = {
        'bills': bills_page,
        'status_filter': status_filter,
    }
    
    return render(request, 'billing/bill_list.html', context)

@login_required
def bill_detail_view(request, bill_id):
    if request.user.role == 'admin':
        bill = get_object_or_404(Bill, id=bill_id)
    elif request.user.role == 'patient':
        try:
            patient = PatientProfile.objects.get(user=request.user)
            bill = get_object_or_404(Bill, id=bill_id, patient=patient)
        except PatientProfile.DoesNotExist:
            messages.warning(request, "Patient profile not found.")
            return redirect('patients:create_profile')
    else:
        messages.error(request, "Access denied.")
        return redirect('authentication:dashboard')
    
    # Get payments for this bill
    payments = Payment.objects.filter(bill=bill).order_by('-payment_date')
    
    # Check if bill has insurance claim
    try:
        insurance_claim = InsuranceClaim.objects.get(bill=bill)
    except InsuranceClaim.DoesNotExist:
        insurance_claim = None
    
    # Forms
    payment_form = PaymentForm(initial={'amount': bill.get_balance()})
    claim_form = None
    if not insurance_claim and request.user.role == 'patient':
        claim_form = InsuranceClaimForm(initial={'claim_amount': bill.get_balance()})
    
    context = {
        'bill': bill,
        'payments': payments,
        'insurance_claim': insurance_claim,
        'payment_form': payment_form,
        'claim_form': claim_form,
    }
    
    return render(request, 'billing/bill_detail.html', context)

@login_required
def make_payment_view(request, bill_id):
    if request.user.role not in ['admin', 'patient']:
        messages.error(request, "Access denied.")
        return redirect('authentication:dashboard')
    
    if request.user.role == 'admin':
        bill = get_object_or_404(Bill, id=bill_id)
    else:
        try:
            patient = PatientProfile.objects.get(user=request.user)
            bill = get_object_or_404(Bill, id=bill_id, patient=patient)
        except PatientProfile.DoesNotExist:
            messages.warning(request, "Patient profile not found.")
            return redirect('patients:create_profile')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.bill = bill
            
            # Validate payment amount
            if payment.amount <= 0:
                messages.error(request, "Payment amount must be greater than zero.")
                return redirect('billing:bill_detail', bill_id=bill.id)
            
            if payment.amount > bill.get_balance():
                messages.error(request, "Payment amount cannot be greater than the balance due.")
                return redirect('billing:bill_detail', bill_id=bill.id)
            
            payment.save()
            messages.success(request, "Payment processed successfully.")
            return redirect('billing:bill_detail', bill_id=bill.id)
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'bill': bill,
    }
    
    return render(request, 'billing/make_payment.html', context)

@login_required
def submit_insurance_claim_view(request, bill_id):
    if request.user.role != 'patient':
        messages.error(request, "Access denied. Only patients can submit insurance claims.")
        return redirect('authentication:dashboard')
    
    try:
        patient = PatientProfile.objects.get(user=request.user)
        bill = get_object_or_404(Bill, id=bill_id, patient=patient)
        
        # Check if bill already has insurance claim
        if InsuranceClaim.objects.filter(bill=bill).exists():
            messages.error(request, "An insurance claim already exists for this bill.")
            return redirect('billing:bill_detail', bill_id=bill.id)
        
        if request.method == 'POST':
            form = InsuranceClaimForm(request.POST)
            if form.is_valid():
                claim = form.save(commit=False)
                claim.bill = bill
                
                # Validate claim amount
                if claim.claim_amount <= 0:
                    messages.error(request, "Claim amount must be greater than zero.")
                    return redirect('billing:bill_detail', bill_id=bill.id)
                
                if claim.claim_amount > bill.get_balance():
                    messages.error(request, "Claim amount cannot be greater than the balance due.")
                    return redirect('billing:bill_detail', bill_id=bill.id)
                
                claim.save()
                messages.success(request, "Insurance claim submitted successfully.")
                return redirect('billing:bill_detail', bill_id=bill.id)
        else:
            form = InsuranceClaimForm()
        
        context = {
            'form': form,
            'bill': bill,
        }
        
        return render(request, 'billing/submit_claim.html', context)
        
    except PatientProfile.DoesNotExist:
        messages.warning(request, "Patient profile not found.")
        return redirect('patients:create_profile')

@login_required
def insurance_claims_view(request):
    if request.user.role != 'insurance_provider':
        messages.error(request, "Access denied. Only insurance providers can access this page.")
        return redirect('authentication:dashboard')
    
    # Get claims based on status filter
    status_filter = request.GET.get('status', '')
    if status_filter:
        claims = InsuranceClaim.objects.filter(status=status_filter).order_by('-submitted_at')
    else:
        claims = InsuranceClaim.objects.all().order_by('-submitted_at')
    
    # Pagination
    paginator = Paginator(claims, 10)
    page = request.GET.get('page')
    claims_page = paginator.get_page(page)
    
    context = {
        'claims': claims_page,
        'status_filter': status_filter,
    }
    
    return render(request, 'billing/insurance_claims.html', context)

@login_required
def process_claim_view(request, claim_id):
    if request.user.role != 'insurance_provider':
        messages.error(request, "Access denied. Only insurance providers can process claims.")
        return redirect('authentication:dashboard')
    
    claim = get_object_or_404(InsuranceClaim, id=claim_id)
    
    if request.method == 'POST':
        form = InsuranceClaimUpdateForm(request.POST, instance=claim)
        if form.is_valid():
            updated_claim = form.save()
            
            # If claim is approved, create a payment from insurance
            if updated_claim.status == 'approved' and updated_claim.approved_amount > 0:
                Payment.objects.create(
                    bill=updated_claim.bill,
                    amount=updated_claim.approved_amount,
                    payment_method='insurance',
                    notes=f"Insurance payment for claim #{updated_claim.id}"
                )
                messages.success(request, "Claim processed and payment created successfully.")
            elif updated_claim.status == 'partially_approved' and updated_claim.approved_amount > 0:
                Payment.objects.create(
                    bill=updated_claim.bill,
                    amount=updated_claim.approved_amount,
                    payment_method='insurance',
                    notes=f"Partial insurance payment for claim #{updated_claim.id}"
                )
                messages.success(request, "Claim partially approved and payment created successfully.")
            else:
                messages.success(request, "Claim status updated successfully.")
            
            return redirect('billing:insurance_claims')
    else:
        form = InsuranceClaimUpdateForm(instance=claim)
    
    context = {
        'form': form,
        'claim': claim,
    }
    
    return render(request, 'billing/process_claim.html', context)
