from django.db import models
from authentication.models import User
from patients.models import PatientProfile

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    education = models.TextField()
    experience_years = models.PositiveIntegerField()
    consulting_fee = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} ({self.specialty})"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='medical_records')
    date = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Record for {self.patient.user.first_name} {self.patient.user.last_name} by Dr. {self.doctor.user.last_name} on {self.date.strftime('%Y-%m-%d')}"

class Prescription(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.medication_name} for {self.record.patient.user.first_name}"
