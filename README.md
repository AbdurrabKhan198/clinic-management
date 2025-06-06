# 🏥 Clinic Management System

A comprehensive Django-based clinic management system designed to streamline patient registration, appointment management, and prescription handling. This system is built for medical professionals to efficiently manage their clinic operations.

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation & Setup](#️-installation--setup)
- [Running the Project](#-running-the-project)
- [Project Structure](#-project-structure)
- [User Roles & Permissions](#-user-roles--permissions)
- [Core Functionality](#-core-functionality)
- [API Endpoints](#-api-endpoints)
- [Database Models](#-database-models)
- [Templates & UI](#-templates--ui)
- [Configuration](#️-configuration)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🔐 Authentication & User Management

- **Custom User Registration**: Healthcare professionals can register with detailed profiles
- **Profile Management**: Doctors can manage their profiles with qualifications, clinic address, and profile pictures
- **Secure Login/Logout**: Django's built-in authentication with custom user model

### 👥 Patient Management

- **Patient Registration**: Comprehensive patient registration with unique ID generation
- **Patient Search**: Search functionality to find existing patients
- **Patient Status Tracking**: Track patients through different stages (Forwarded to Doctor, Prescription Done)
- **Patient History**: Maintain complete patient history and records

### 💊 Prescription Management

- **Digital Prescriptions**: Complete prescription management system
- **Medication Tracking**: Structured medication entries with dosage information
- **Common Entries**: Auto-complete functionality for common medical terms
- **Prescription Templates**: Reusable prescription components

### 📊 Workflow Management

- **Patient Flow**: Seamless patient flow from registration to prescription
- **Status Updates**: Real-time status updates for patient progress
- **Assignment System**: Assign patients to specific doctors

## 🛠 Technology Stack

- **Backend**: Django 5.2.1
- **Database**: SQLite (Development) / PostgreSQL (Production Ready)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Image Handling**: Pillow 11.2.1
- **Authentication**: Django's built-in auth system with custom user model
- **Deployment**: Production-ready configuration for DigitalOcean

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd clinic-management
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv clinic_env

# Activate virtual environment
# On Linux/Mac:
source clinic_env/bin/activate

# On Windows:
clinic_env\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 6: Collect Static Files (For Production)

```bash
python manage.py collectstatic
```

## 🚀 Running the Project

### Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### Production Deployment

The project is configured for deployment with the following production settings:

- **Allowed Hosts**: `143.110.182.37`, `www.zospital.in`, `zospital.in`
- **Static Files**: Configured for production serving
- **Media Files**: Configured for user uploads

## 📁 Project Structure

```
clinic-management/
├── crm/                    # Main Django project directory
│   ├── __init__.py
│   ├── settings.py         # Project settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
│
├── home/                   # Main application directory
│   ├── migrations/         # Database migrations
│   ├── static/            # Static files (CSS, JS, images)
│   ├── templates/home/    # HTML templates
│   ├── __init__.py
│   ├── admin.py           # Django admin configuration
│   ├── apps.py            # App configuration
│   ├── forms.py           # Django forms
│   ├── models.py          # Database models
│   ├── urls.py            # App URL patterns
│   └── views.py           # View functions
│
├── media/                  # User uploaded files
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 👤 User Roles & Permissions

### Healthcare Professional (Doctor/Staff)

- Register and manage profile
- Add new patients
- View and manage assigned patients
- Create and manage prescriptions
- Search patient history
- Access admin panel (superuser)

### Patient Flow States

1. **Registration**: Patient is added to the system
2. **Forwarded**: Patient is forwarded to doctor
3. **Done**: Prescription completed

## 🔧 Core Functionality

### 1. User Authentication System

```python
# Custom User Model with additional fields
class CustomUser(AbstractUser):
    name = models.CharField(max_length=150)
    qualification = models.CharField(max_length=255)
    clinic_address = models.TextField()
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='profile_pics/')
```

### 2. Patient Management System

- **Unique Patient ID Generation**: Each patient gets a unique ID (`zospital_{uuid}_lko`)
- **Comprehensive Patient Records**: Including demographics, medical history, and prescription details
- **Status Tracking**: Workflow management through patient states

### 3. Prescription Management

- **Digital Prescription Forms**: Complete prescription creation interface
- **Medication Management**: Structured medication entries with dosage
- **Auto-complete Features**: Common medical terms for faster data entry
- **Prescription History**: Complete prescription tracking

### 4. Search & Filter System

- **Patient Search**: Search by name, phone, or ID
- **Status Filters**: Filter patients by status
- **Date Filters**: Filter by creation date or visit date

## 🌐 API Endpoints

### Authentication Endpoints

- `GET/POST /` - User registration (signup)
- `GET/POST /login/` - User login
- `POST /logout/` - User logout

### Patient Management Endpoints

- `GET/POST /add-patient/` - Add new patient
- `GET /existing-patients/` - View existing patients with search
- `GET /patient/<id>/` - View patient details
- `GET/POST /patient/<id>/edit/` - Edit patient information

### Prescription Endpoints

- `GET/POST /add-prescription/<patient_id>/` - Create/edit prescription
- `POST /mark-done/<patient_id>/` - Mark prescription as complete

### Profile Management

- `GET /profile/` - View user profile
- `GET /welcome/` - Dashboard/welcome page

### Utility Endpoints

- `POST /save-common-entry/` - Save common medical terms
- `GET /autocomplete-common-entries/` - Auto-complete API

## 🗄️ Database Models

### 1. CustomUser Model

Extended Django user model for healthcare professionals with additional fields for medical practice information.

### 2. Patient Model

Comprehensive patient model including:

- **Basic Information**: Name, age, gender, contact details
- **Medical Information**: Height, weight, BP, medical history
- **Prescription Fields**: Complaints, diagnosis, treatment plan, medications
- **Workflow Fields**: Status, assigned doctor, creation details

### 3. MedicationEntry Model

Structured medication tracking with:

- Medicine name
- Dosage frequency (once/twice/thrice daily)
- Patient association
- Creation timestamp

### 4. CommonEntry Model

Reusable medical terms for different prescription fields to improve efficiency and consistency.

## 🎨 Templates & UI

### Template Structure

- **base.html**: Base template with Bootstrap styling
- **signup.html**: User registration form
- **login.html**: User authentication form
- **welcome.html**: Dashboard with navigation
- **add_patient.html**: Patient registration form
- **existing_patients.html**: Patient listing with search
- **patient_prescription.html**: Prescription creation interface
- **view_patient.html**: Patient details view
- **view_profile.html**: User profile display

### UI Features

- **Responsive Design**: Bootstrap-based responsive interface
- **Modern Styling**: Clean, professional medical interface
- **Dynamic Forms**: JavaScript-enhanced forms for better UX
- **Auto-complete**: Real-time suggestions for medical terms
- **Search Functionality**: Instant patient search capabilities

## ⚙️ Configuration

### Development Settings

- **DEBUG**: Enabled for development
- **Database**: SQLite for local development
- **Static Files**: Development serving enabled

### Production Settings

- **ALLOWED_HOSTS**: Configured for specific domains
- **Static Files**: Production-ready static file serving
- **Media Files**: User upload handling
- **Security**: Django security features enabled

### Environment Variables (Recommended)

Create a `.env` file for sensitive settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## 🔒 Security Features

- **CSRF Protection**: Built-in CSRF protection for all forms
- **User Authentication**: Secure login/logout functionality
- **Permission System**: Role-based access control
- **File Upload Security**: Secure handling of profile pictures
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **XSS Protection**: Template system prevents XSS attacks

## 📈 Future Enhancements

### Planned Features

- **Appointment Scheduling**: Calendar-based appointment system
- **Billing Integration**: Invoice and payment tracking
- **Lab Reports**: Integration with laboratory systems
- **SMS/Email Notifications**: Patient communication system
- **Analytics Dashboard**: Clinic performance metrics
- **Mobile App**: React Native mobile application
- **API Development**: RESTful API for third-party integrations


## 📋 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test home

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for healthcare professionals**
