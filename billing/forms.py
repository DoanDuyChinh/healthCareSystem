from django import forms
from .models import Bill, Payment, InsuranceClaim
from datetime import datetime, timedelta
from django.utils import timezone

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['patient', 'bill_type', 'amount', 'description', 'due_date']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'bill_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default due date to 30 days from now
        if not self.instance.due_date:
            self.fields['due_date'].initial = timezone.now() + timedelta(days=30)

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'transaction_id', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class InsuranceClaimForm(forms.ModelForm):
    class Meta:
        model = InsuranceClaim
        fields = ['insurance_provider', 'policy_number', 'claim_amount', 'notes']
        widgets = {
            'insurance_provider': forms.TextInput(attrs={'class': 'form-control'}),
            'policy_number': forms.TextInput(attrs={'class': 'form-control'}),
            'claim_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class InsuranceClaimUpdateForm(forms.ModelForm):
    class Meta:
        model = InsuranceClaim
        fields = ['status', 'approved_amount', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'approved_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
