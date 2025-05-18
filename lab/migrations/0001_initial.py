from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('patients', '0001_initial'),
        ('doctors', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='LabTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_type', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('ordered', 'Ordered'), ('sample_collected', 'Sample Collected'), ('processing', 'Processing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='ordered', max_length=20)),
                ('ordered_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('result', models.TextField(blank=True, null=True)),
                ('result_file', models.FileField(blank=True, null=True, upload_to='lab_results/')),
                ('technician_notes', models.TextField(blank=True, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_tests', to='doctors.doctorprofile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lab_tests', to='patients.patientprofile')),
            ],
        ),
    ]
