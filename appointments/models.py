from django.db import models
from patients.models import PatientProfile
from doctors.models import DoctorProfile
from django.utils import timezone

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.patient.user.first_name} with Dr. {self.doctor.user.last_name} on {self.date.strftime('%Y-%m-%d %H:%M')}"
    
    def is_past_due(self):
        return timezone.now() > self.date
    
    def save(self, *args, **kwargs):
        # Track status changes - with safer implementation for migration period
        if self.pk is not None:
            try:
                old_instance = Appointment.objects.get(pk=self.pk)
                old_status = getattr(old_instance, 'status', None)
                if old_status != 'completed' and self.status == 'completed':
                    self.completed_at = timezone.now()
            except Exception:
                # If there's any issue (like missing column during migration), 
                # just set the completed_at field if status is completed
                if self.status == 'completed' and not self.completed_at:
                    self.completed_at = timezone.now()
        
        super().save(*args, **kwargs)
