from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('bills/', views.bill_list_view, name='bill_list'),
    path('bills/<int:bill_id>/', views.bill_detail_view, name='bill_detail'),
    path('generate-bill/', views.generate_bill_view, name='generate_bill'),
    path('make-payment/<int:bill_id>/', views.make_payment_view, name='make_payment'),
    path('submit-claim/<int:bill_id>/', views.submit_insurance_claim_view, name='submit_claim'),
    path('insurance-claims/', views.insurance_claims_view, name='insurance_claims'),
    path('process-claim/<int:claim_id>/', views.process_claim_view, name='process_claim'),
]
