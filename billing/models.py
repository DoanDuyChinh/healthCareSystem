from django.db import models
from patients.models import PatientProfile
from doctors.models import MedicalRecord
from pharmacy.models import MedicineDispense
from lab.models import LabTest
from appointments.models import Appointment
from django.utils import timezone

class Bill(models.Model):
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    BILL_TYPE_CHOICES = [
        ('appointment', 'Appointment'),
        ('medicine', 'Medicine'),
        ('lab_test', 'Lab Test'),
        ('other', 'Other'),
    ]
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='bills')
    bill_type = models.CharField(max_length=20, choices=BILL_TYPE_CHOICES)
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='bill')
    medicine_dispense = models.OneToOneField(MedicineDispense, on_delete=models.SET_NULL, null=True, blank=True, related_name='bill')
    lab_test = models.OneToOneField(LabTest, on_delete=models.SET_NULL, null=True, blank=True, related_name='bill')
    medical_record = models.OneToOneField(MedicalRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='bill')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Bill #{self.id} - {self.patient.user.first_name} {self.patient.user.last_name} - ${self.amount}"
    
    def get_balance(self):
        return self.amount - self.amount_paid
    
    def is_overdue(self):
        if self.due_date:
            return timezone.now() > self.due_date and self.status != 'paid'
        return False

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('insurance', 'Insurance'),
    ]
    
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Payment of ${self.amount} for Bill #{self.bill.id}"
    
    def save(self, *args, **kwargs):
        # Update the bill's amount_paid and status when payment is saved
        super().save(*args, **kwargs)
        
        # Update bill
        bill = self.bill
        total_paid = bill.payments.aggregate(models.Sum('amount'))['amount__sum'] or 0
        bill.amount_paid = total_paid
        
        if total_paid >= bill.amount:
            bill.status = 'paid'
        elif total_paid > 0:
            bill.status = 'partially_paid'
        else:
            bill.status = 'unpaid'
            
        bill.save()

class InsuranceClaim(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('approved', 'Approved'),
        ('partially_approved', 'Partially Approved'),
        ('rejected', 'Rejected'),
    ]
    
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE, related_name='insurance_claim')
    insurance_provider = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=100)
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Insurance Claim #{self.id} for Bill #{self.bill.id}"
