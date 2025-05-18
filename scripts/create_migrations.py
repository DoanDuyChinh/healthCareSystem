"""
Script to create initial migrations directory and files without requiring Django setup
"""
import os
import shutil
from pathlib import Path

def main():
    # Create the migrations directory if it doesn't exist
    migrations_dir = Path('authentication/migrations')
    migrations_dir.mkdir(exist_ok=True, parents=True)
    
    # Create __init__.py
    init_file = migrations_dir / '__init__.py'
    if not init_file.exists():
        with open(init_file, 'w') as f:
            pass
        print(f"Created {init_file}")
    
    # Copy the initial migration file if it exists in the scripts directory
    template_path = Path('scripts/migration_templates/0001_initial.py')
    if template_path.exists():
        shutil.copy(template_path, migrations_dir / '0001_initial.py')
        print(f"Copied initial migration template to {migrations_dir / '0001_initial.py'}")
    else:
        print("No migration template found. Create a migration manually or run makemigrations.")
    
    print("Migration directory setup complete!")

if __name__ == "__main__":
    main()
