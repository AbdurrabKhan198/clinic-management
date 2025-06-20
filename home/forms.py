from django import forms
from .models import Patient, MedicationEntry


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'phone', 'age', 'height', 'weight', 'BP', 'gender', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'age': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
            'height': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'step': '0.01', 'placeholder': 'Enter height in cm'}),  # step add kiya
            'weight': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter weight in kgs'}),
            'BP': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'gender': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'chief_complaints',
            'investigation',
            'advice',
            'examination_findings',
            'diagnosis',
            'treatment_plan',
            'next_visit_date',
        ]
        widgets = {
            'next_visit_date': forms.DateInput(attrs={'type': 'date'}),
        }


# ---------------------------
# Medication form and formset
# ---------------------------
class MedicationEntryForm(forms.ModelForm):
    class Meta:
        model = MedicationEntry
        fields = ['medicine_name', 'dosage']
        widgets = {
            'medicine_name': forms.TextInput(attrs={'placeholder': 'e.g. Paracetamol'}),
            'dosage': forms.Select(choices=[
                ('once', 'Once a day'),
                ('twice', 'Twice a day'),
                ('thrice', 'Thrice a day'),
            ])
        }


# Formset to handle multiple medicine entries dynamically
MedicationEntryFormSet = forms.inlineformset_factory(
    parent_model=Patient,
    model=MedicationEntry,
    form=MedicationEntryForm,
    extra=1,  # Can be adjusted dynamically via JS too
    can_delete=True
)
