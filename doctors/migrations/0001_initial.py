from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('authentication', '0001_initial'),
        ('patients', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='DoctorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialty', models.CharField(max_length=100)),
                ('license_number', models.CharField(max_length=50)),
                ('education', models.TextField()),
                ('experience_years', models.PositiveIntegerField()),
                ('consulting_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to='authentication.user')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('symptoms', models.TextField()),
                ('diagnosis', models.TextField()),
                ('treatment_plan', models.TextField()),
                ('follow_up_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to='doctors.doctorprofile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to='patients.patientprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medication_name', models.CharField(max_length=100)),
                ('dosage', models.CharField(max_length=100)),
                ('frequency', models.CharField(max_length=100)),
                ('duration', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True, null=True)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='doctors.medicalrecord')),
            ],
        ),
    ]
