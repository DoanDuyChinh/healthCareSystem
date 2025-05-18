from django.db import models
from patients.models import PatientProfile
from doctors.models import DoctorProfile
from django.utils import timezone

class LabTest(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('sample_collected', 'Sample Collected'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='lab_tests')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='ordered_tests')
    test_type = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')
    ordered_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    result = models.TextField(blank=True, null=True)
    result_file = models.FileField(upload_to='lab_results/', blank=True, null=True)
    technician_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.test_type} for {self.patient.user.first_name} {self.patient.user.last_name}"
    
    def mark_as_completed(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
