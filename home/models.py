from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid

# Custom user model for doctors/staff with extra fields
class CustomUser(AbstractUser):
    name = models.CharField(max_length=150)
    qualification = models.CharField(max_length=255)
    clinic_address = models.TextField()
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username


# Function to generate unique patient ID
def generate_custom_id():
    return f"zospital_{uuid.uuid4().hex[:6]}_lko"


class Patient(models.Model):
    STATUS_CHOICES = [
        ('forwarded', 'Forwarded to Doctor'),
        ('done', 'Prescription Done'),
    ]

    custom_id = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        editable=False,
        default=generate_custom_id  # ✅ default added to prevent migration issue
    )
    name = models.CharField(max_length=100)
    height = models.CharField(max_length=20, default='N/A')
    weight = models.CharField(max_length=20, default='N/A')
    BP = models.CharField(max_length=10,default='N/A')
    phone = models.CharField(max_length=15)
    age = models.CharField(max_length=25, default='N/A')
    gender = models.CharField(max_length=10)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='forwarded')
    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='patients_created'
    )
    assigned_doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='patients_assigned'
    )

    # Prescription details
    chief_complaints = models.TextField(blank=True, null=True)
    investigation = models.TextField(blank=True, null=True)
    advice = models.TextField(blank=True, null=True)
    examination_findings = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    treatment_plan = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)  # For custom entries
    next_visit_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


# Structured medications with dosage per patient
class MedicationEntry(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medication_entries')
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(
        max_length=50,
        choices=[
            ('once', 'Once a day'),
            ('twice', 'Twice a day'),
            ('thrice', 'Thrice a day'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine_name} ({self.dosage}) for {self.patient.name}"
