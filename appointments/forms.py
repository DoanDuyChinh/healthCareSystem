from django import forms
from .models import Appointment
from doctors.models import DoctorProfile
from django.utils import timezone
import datetime

class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=DoctorProfile.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'reason']
        widgets = {
            'date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'
            ),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set minimum date to tomorrow
        self.fields['date'].widget.attrs['min'] = (
            timezone.now() + datetime.timedelta(days=1)
        ).strftime('%Y-%m-%dT%H:%M')

class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
