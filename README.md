# Healthcare Management System

A comprehensive healthcare management system built with Django, featuring patient records, appointments, billing, pharmacy, and lab management.

## Features

- Multi-user authentication with different roles (patient, doctor, admin, etc.)
- Patient profile and medical records
- Appointment scheduling
- Prescription management
- Laboratory test ordering and results
- Pharmacy inventory and medicine dispensing
- Billing and insurance claims
- Admin dashboard with reports

## Technology Stack

- **Backend**: Django
- **Frontend**: Django Templates, Bootstrap 5, Font Awesome
- **Database**: PostgreSQL (Docker) / SQLite (Development)
- **Deployment**: Docker, Nginx, Gunicorn

## Prerequisites

- Docker and Docker Compose
- Git

## Running with Docker

1. Clone the repository:
   ```
   git clone <repository-url>
   cd healthcare_system
   ```

2. Build and start the containers:
   ```
   docker-compose up -d --build
   ```

3. The application will be available at:
   ```
   http://localhost
   ```

4. Default admin credentials:
   - Username: admin
   - Password: admin

## Development Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

## Project Structure

- **authentication**: User authentication and profile management
- **patients**: Patient profiles and medical history
- **doctors**: Doctor profiles and patient management
- **appointments**: Scheduling and managing appointments
- **pharmacy**: Medicine inventory and prescription fulfillment
- **lab**: Lab test ordering and results
- **billing**: Invoices, payments, and insurance claims
- **adminpanel**: Administrative dashboard and reports

## License

This project is licensed under the MIT License - see the LICENSE file for details.
