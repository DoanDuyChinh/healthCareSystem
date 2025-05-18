from django.db import models
from authentication.models import User
from doctors.models import Prescription
from django.utils import timezone

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    manufacturer = models.CharField(max_length=100)
    requires_prescription = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def is_in_stock(self):
        return self.stock_quantity > 0

class MedicineDispense(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('dispensed', 'Dispensed'),
        ('cancelled', 'Cancelled'),
    ]
    
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='dispenses')
    pharmacist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dispenses')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='dispenses')
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    dispensed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.medicine.name} for {self.prescription.record.patient.user.first_name}"
    
    def dispense(self, pharmacist):
        if self.status != 'pending':
            return False
        
        if self.medicine.stock_quantity < self.quantity:
            return False
        
        self.pharmacist = pharmacist
        self.status = 'dispensed'
        self.dispensed_at = timezone.now()
        self.save()
        
        # Reduce medicine stock
        self.medicine.stock_quantity -= self.quantity
        self.medicine.save()
        
        return True
