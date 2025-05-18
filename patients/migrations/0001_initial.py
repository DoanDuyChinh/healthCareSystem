from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('authentication', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='PatientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
                ('blood_type', models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3, null=True)),
                ('height', models.FloatField(blank=True, help_text='Height in cm', null=True)),
                ('weight', models.FloatField(blank=True, help_text='Weight in kg', null=True)),
                ('allergies', models.TextField(blank=True, null=True)),
                ('chronic_diseases', models.TextField(blank=True, null=True)),
                ('emergency_contact_name', models.CharField(blank=True, max_length=100, null=True)),
                ('emergency_contact_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_profile', to='authentication.user')),
            ],
        ),
    ]
