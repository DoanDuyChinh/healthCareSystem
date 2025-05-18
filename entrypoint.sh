#!/bin/bash

# Exit on error
set -e

# Wait for database
echo "Waiting for database..."
while ! pg_isready -h db -p 5432 -q -U postgres; do
  sleep 1
done
echo "Database is ready!"

# Reset database if there are migration issues
if [ "${RESET_DB:-false}" = "true" ]; then
  echo "Resetting database..."
  python -c "
import psycopg2
conn = psycopg2.connect(
    dbname='healthcare',
    user='postgres',
    password='postgres',
    host='db',
    port='5432'
)
conn.autocommit = True
cursor = conn.cursor()
cursor.execute('DROP SCHEMA public CASCADE;')
cursor.execute('CREATE SCHEMA public;')
cursor.execute('GRANT ALL ON SCHEMA public TO postgres;')
cursor.execute('GRANT ALL ON SCHEMA public TO public;')
conn.close()
"
  echo "Database reset complete."
fi

# Clean up all migration files and start fresh
echo "Setting up migrations directories..."
for app in authentication patients doctors appointments pharmacy lab billing adminpanel; do
  mkdir -p ${app}/migrations
  touch ${app}/migrations/__init__.py
  echo "Created migrations directory for ${app}"
  
  # If CLEAN_MIGRATIONS is true, remove all migration files except __init__.py
  if [ "${CLEAN_MIGRATIONS:-false}" = "true" ]; then
    find ${app}/migrations -type f -not -name "__init__.py" -delete
    echo "Cleaned migrations for ${app}"
  fi
done

# Create initial migration for authentication app
echo "Creating initial migration for authentication app..."
cat > authentication/migrations/0001_initial.py << 'EOF'
from django.db import migrations, models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]
    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('patient', 'Patient'), ('doctor', 'Doctor'), ('nurse', 'Nurse'), ('admin', 'Admin'), ('pharmacist', 'Pharmacist'), ('lab_technician', 'Lab Technician'), ('insurance_provider', 'Insurance Provider')], max_length=20)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
EOF
echo "Created authentication initial migration"

# Create initial migration for patients app
echo "Creating initial migration for patients app..."
cat > patients/migrations/0001_initial.py << 'EOF'
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
EOF
echo "Created patients initial migration"

# Create initial migration for doctors app
echo "Creating initial migration for doctors app..."
cat > doctors/migrations/0001_initial.py << 'EOF'
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
EOF
echo "Created doctors initial migration"

# Create initial migration for appointments app
echo "Creating initial migration for appointments app..."
cat > appointments/migrations/0001_initial.py << 'EOF'
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
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('reason', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='doctors.doctorprofile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='patients.patientprofile')),
            ],
        ),
    ]
EOF
echo "Created appointments initial migration"

# Create initial migration for pharmacy app
echo "Creating initial migration for pharmacy app..."
cat > pharmacy/migrations/0001_initial.py << 'EOF'
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
EOF
echo "Created pharmacy initial migration"

# Create initial migration for lab app
echo "Creating initial migration for lab app..."
cat > lab/migrations/0001_initial.py << 'EOF'
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
EOF
echo "Created lab initial migration"

# Create initial migration for billing app
echo "Creating initial migration for billing app..."
cat > billing/migrations/0001_initial.py << 'EOF'
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
EOF
echo "Created billing initial migration"

# Create initial migration for chatbot app
echo "Creating initial migration for chatbot app..."
cat > chatbot/migrations/0001_initial.py << 'EOF'
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='New Conversation', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to='authentication.user')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(choices=[('user', 'User'), ('bot', 'Bot')], max_length=10)),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chatbot.conversation')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]
EOF
echo "Created chatbot initial migration"

# Apply database migrations in the correct order
echo "Applying database migrations..."

# First migrate auth and contenttypes models
python manage.py migrate auth --noinput
python manage.py migrate contenttypes --noinput

# Then migrate the authentication app with our custom user model
python manage.py migrate authentication --noinput

# Then migrate all other apps one by one to ensure proper dependencies
python manage.py migrate patients --noinput
python manage.py migrate doctors --noinput
python manage.py migrate appointments --noinput
python manage.py migrate pharmacy --noinput
python manage.py migrate lab --noinput
python manage.py migrate billing --noinput
python manage.py migrate adminpanel --noinput
python manage.py migrate chatbot --noinput

# Final migration to catch any dependencies between apps
python manage.py migrate --noinput

# Create static directories if they don't exist
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if not exists
echo "Creating superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin', role='admin')
    print('Superuser created.')
else:
    print('Superuser already exists.')
END

# Clear expired sessions
echo "Clearing expired sessions..."
python manage.py clearsessions

# Start server
echo "Starting server..."
exec gunicorn healthcare_system.wsgi:application --bind 0.0.0.0:8000
