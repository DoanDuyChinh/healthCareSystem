from django import forms
from .models import LabTest

class OrderLabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ['test_type', 'description']
        widgets = {
            'test_type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class UpdateLabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ['status', 'result', 'result_file', 'technician_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'result': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'result_file': forms.FileInput(attrs={'class': 'form-control'}),
            'technician_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
