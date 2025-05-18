"""
Script to generate clean migrations for the authentication app
"""
import os
import sys
import shutil
from pathlib import Path

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_system.settings')
import django
django.setup()

from django.core.management import call_command

def main():
    # Path to migrations directory
    migrations_dir = Path('authentication/migrations')
    
    # Backup existing migrations if needed
    if migrations_dir.exists() and any(migrations_dir.iterdir()):
        backup_dir = migrations_dir.with_name('migrations_backup')
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(migrations_dir, backup_dir)
        print(f"Backed up existing migrations to {backup_dir}")
    
    # Remove existing migrations except __init__.py
    if migrations_dir.exists():
        for file_path in migrations_dir.glob('*.py'):
            if file_path.name != '__init__.py':
                file_path.unlink()
                print(f"Removed {file_path}")
    
    # Create migrations directory if it doesn't exist
    migrations_dir.mkdir(exist_ok=True)
    init_file = migrations_dir / '__init__.py'
    if not init_file.exists():
        with open(init_file, 'w') as f:
            pass
    
    # Generate new migrations
    print("Generating new migrations...")
    call_command('makemigrations', 'authentication')
    
    print("Migrations generated successfully!")

if __name__ == "__main__":
    main()
