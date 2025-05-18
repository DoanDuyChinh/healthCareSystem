from django import forms
from .models import Medicine, MedicineDispense

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'description', 'unit_price', 'stock_quantity', 'manufacturer', 'requires_prescription']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'requires_prescription': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MedicineDispenseForm(forms.ModelForm):
    class Meta:
        model = MedicineDispense
        fields = ['medicine', 'quantity', 'notes']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class UpdateMedicineDispenseForm(forms.ModelForm):
    class Meta:
        model = MedicineDispense
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
