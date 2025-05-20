# Real Estate Visit Management System

A web application for managing real estate visits and appointments.

## Features

### Dashboard
- Overview of today's visits
- Upcoming visits
- Recent visits
- Quick access to visit creation
- User management
- Excel export functionality

### Visit Management
- Create, edit, and delete visits
- Schedule visits with different types (in-person, phone, email)
- Track visit status (scheduled, completed, cancelled, forgotten)
- Add visit details including:
  - Title
  - Name
  - Address
  - Description
  - Transaction type (buy, rent, lease, purchase)
  - Price
  - Email and phone contact
  - Comments
- View contract status directly from visit details

### Contract Management
- Create and manage property contracts
- Track contract status (draft, active, completed, cancelled)
- Store important contract details:
  - Property information
  - Parties involved
  - Contract terms and conditions
  - Signing date and expiration
  - Payment schedules
  - Attachments and documents
- Link contracts to related visits and properties
- Generate contract PDFs
- Send contracts for e-signature

### Reports
- View completed visits and contracts
- Filter contracts by status and date range
- Export contract data to Excel
- Filter visits by:
  - Date range
  - Visit type
- Add unplanned visits manually
- Export visits to Excel
- Statistics about completed visits

### User Management
- Create and manage users
- Change user passwords
- Assign staff status
- Delete users

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Requirements

- Python 3.10+
- Django 5.2.1
- openpyxl (for Excel export)
- reportlab (for PDF generation)
- django-crispy-forms (for better form rendering)
- Bootstrap 5
- Font Awesome 6

## License

MIT License
