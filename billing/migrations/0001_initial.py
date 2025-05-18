from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('patients', '0001_initial'),
        ('appointments', '0001_initial'),
        ('pharmacy', '0001_initial'),
        ('lab', '0001_initial'),
        ('doctors', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_type', models.CharField(choices=[('appointment', 'Appointment'), ('medicine', 'Medicine'), ('lab_test', 'Lab Test'), ('other', 'Other')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('unpaid', 'Unpaid'), ('partially_paid', 'Partially Paid'), ('paid', 'Paid'), ('cancelled', 'Cancelled')], default='unpaid', max_length=20)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('appointment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bill', to='appointments.appointment')),
                ('lab_test', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bill', to='lab.labtest')),
                ('medical_record', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bill', to='doctors.medicalrecord')),
                ('medicine_dispense', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bill', to='pharmacy.medicinedispense')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='patients.patientprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('bank_transfer', 'Bank Transfer'), ('insurance', 'Insurance')], max_length=20)),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='billing.bill')),
            ],
        ),
        migrations.CreateModel(
            name='InsuranceClaim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insurance_provider', models.CharField(max_length=100)),
                ('policy_number', models.CharField(max_length=100)),
                ('claim_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('approved_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('in_progress', 'In Progress'), ('approved', 'Approved'), ('partially_approved', 'Partially Approved'), ('rejected', 'Rejected')], default='submitted', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('bill', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='insurance_claim', to='billing.bill')),
            ],
        ),
    ]
