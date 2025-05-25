from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Patient, CustomUser, MedicationEntry


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'qualification', 'clinic_address', 'phone', 'profile_pic')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('name', 'qualification', 'clinic_address', 'phone', 'profile_pic')}),
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'phone', 'age', 'gender', 'status', 
        'assigned_doctor', 'created_by', 'created_at'
    )
    list_filter = ('status', 'gender', 'assigned_doctor')
    search_fields = ('name', 'phone', 'created_by__username', 'assigned_doctor__username')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'phone', 'age', 'gender', 'address')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'created_by', 'assigned_doctor', 'created_at')
        }),
        ('Prescription', {
            'classes': ('collapse',),
            'fields': (
                'chief_complaints', 'investigation', 'advice',
                'examination_findings', 'diagnosis', 'treatment_plan',
                'medications', 'next_visit_date',
            )
        }),
    )


@admin.register(MedicationEntry)
class MedicationEntryAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medicine_name', 'dosage', 'created_at')
    list_filter = ('dosage', 'medicine_name')
    search_fields = ('patient__name', 'medicine_name')
    readonly_fields = ('created_at',)
