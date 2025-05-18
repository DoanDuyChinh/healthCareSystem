from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('authentication', '0001_initial'),
        ('doctors', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock_quantity', models.PositiveIntegerField(default=0)),
                ('manufacturer', models.CharField(max_length=100)),
                ('requires_prescription', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MedicineDispense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('dispensed', 'Dispensed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('notes', models.TextField(blank=True, null=True)),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('dispensed_at', models.DateTimeField(blank=True, null=True)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dispenses', to='pharmacy.medicine')),
                ('pharmacist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dispenses', to='authentication.user')),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dispenses', to='doctors.prescription')),
            ],
        ),
    ]
