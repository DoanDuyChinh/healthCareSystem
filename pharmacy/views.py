from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Medicine, MedicineDispense
from .forms import MedicineForm, MedicineDispenseForm, UpdateMedicineDispenseForm
from doctors.models import Prescription
from patients.models import PatientProfile

@login_required
def dashboard_view(request):
    if request.user.role != 'pharmacist':
        messages.error(request, "Access denied. Only pharmacists can access this page.")
        return redirect('authentication:dashboard')
    
    # Get pending dispenses
    pending_dispenses = MedicineDispense.objects.filter(
        status='pending'
    ).order_by('requested_at')
    
    # Get recently dispensed medications
    recent_dispenses = MedicineDispense.objects.filter(
        status='dispensed'
    ).order_by('-dispensed_at')[:10]
    
    # Get medicines with low stock
    low_stock_medicines = Medicine.objects.filter(
        stock_quantity__lt=10
    ).order_by('stock_quantity')
    
    context = {
        'pending_dispenses': pending_dispenses,
        'recent_dispenses': recent_dispenses,
        'low_stock_medicines': low_stock_medicines,
    }
    
    return render(request, 'pharmacy/dashboard.html', context)

@login_required
def medicine_list_view(request):
    if request.user.role != 'pharmacist':
        messages.error(request, "Access denied. Only pharmacists can access this page.")
        return redirect('authentication:dashboard')
    
    search_query = request.GET.get('search', '')
    if search_query:
        medicines = Medicine.objects.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(manufacturer__icontains=search_query)
        ).order_by('name')
    else:
        medicines = Medicine.objects.all().order_by('name')
    
    paginator = Paginator(medicines, 10)
    page = request.GET.get('page')
    medicines_page = paginator.get_page(page)
    
    context = {
        'medicines': medicines_page,
        'search_query': search_query,
    }
    
    return render(request, 'pharmacy/medicine_list.html', context)

@login_required
def add_medicine_view(request):
    if request.user.role != 'pharmacist':
        messages.error(request, "Access denied. Only pharmacists can access this page.")
        return redirect('authentication:dashboard')
    
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Medicine added successfully.")
            return redirect('pharmacy:medicine_list')
    else:
        form = MedicineForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'pharmacy/add_medicine.html', context)

@login_required
def edit_medicine_view(request, medicine_id):
    if request.user.role != 'pharmacist':
        messages.error(request, "Access denied. Only pharmacists can access this page.")
        return redirect('authentication:dashboard')
    
    medicine = get_object_or_404(Medicine, id=medicine_id)
    
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, "Medicine updated successfully.")
            return redirect('pharmacy:medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    
    context = {
        'form': form,
        'medicine': medicine,
    }
    
    return render(request, 'pharmacy/edit_medicine.html', context)

@login_required
def dispense_medicine_view(request, dispense_id):
    if request.user.role != 'pharmacist':
        messages.error(request, "Access denied. Only pharmacists can access this page.")
        return redirect('authentication:dashboard')
    
    dispense = get_object_or_404(MedicineDispense, id=dispense_id, status='pending')
    
    if request.method == 'POST':
        form = UpdateMedicineDispenseForm(request.POST, instance=dispense)
        if form.is_valid():
            if form.cleaned_data['status'] == 'dispensed':
                success = dispense.dispense(request.user)
                if success:
                    messages.success(request, "Medicine dispensed successfully.")
                else:
                    messages.error(request, "Failed to dispense. Check if there's enough stock.")
            else:
                form.save()
                messages.success(request, "Dispense status updated.")
            return redirect('pharmacy:dashboard')
    else:
        form = UpdateMedicineDispenseForm(instance=dispense)
    
    context = {
        'form': form,
        'dispense': dispense,
    }
    
    return render(request, 'pharmacy/dispense_medicine.html', context)

@login_required
def prescription_view(request, prescription_id):
    if request.user.role not in ['doctor', 'pharmacist', 'patient']:
        messages.error(request, "Access denied.")
        return redirect('authentication:dashboard')
    
    prescription = get_object_or_404(Prescription, id=prescription_id)
    patient = prescription.record.patient
    
    # Check permissions
    if request.user.role == 'doctor' and prescription.record.doctor.user != request.user:
        messages.error(request, "Access denied. You are not the prescribing doctor.")
        return redirect('authentication:dashboard')
    
    if request.user.role == 'patient' and patient.user != request.user:
        messages.error(request, "Access denied. This prescription is not yours.")
        return redirect('authentication:dashboard')
    
    dispenses = MedicineDispense.objects.filter(prescription=prescription)
    
    context = {
        'prescription': prescription,
        'patient': patient,
        'dispenses': dispenses,
    }
    
    return render(request, 'pharmacy/prescription_view.html', context)

@login_required
def request_medicine_view(request, prescription_id):
    if request.user.role != 'patient':
        messages.error(request, "Access denied. Only patients can request medicines.")
        return redirect('authentication:dashboard')
    
    prescription = get_object_or_404(Prescription, id=prescription_id)
    patient = prescription.record.patient
    
    # Verify this prescription belongs to the requesting patient
    if patient.user != request.user:
        messages.error(request, "Access denied. This prescription is not yours.")
        return redirect('authentication:dashboard')
    
    if request.method == 'POST':
        form = MedicineDispenseForm(request.POST)
        if form.is_valid():
            dispense = form.save(commit=False)
            dispense.prescription = prescription
            
            # Check if medicine requires prescription
            if dispense.medicine.requires_prescription and prescription is None:
                messages.error(request, "This medicine requires a valid prescription.")
                return redirect('patients:dashboard')
            
            # Check if we have enough stock
            if dispense.quantity > dispense.medicine.stock_quantity:
                messages.error(request, "Not enough medicine in stock.")
                return redirect('pharmacy:prescription_view', prescription_id=prescription.id)
            
            dispense.save()
            messages.success(request, "Medicine request submitted successfully.")
            return redirect('pharmacy:prescription_view', prescription_id=prescription.id)
    else:
        form = MedicineDispenseForm()
    
    context = {
        'form': form,
        'prescription': prescription,
    }
    
    return render(request, 'pharmacy/request_medicine.html', context)
