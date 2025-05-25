from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PatientForm, PrescriptionForm  # You need to create PrescriptionForm
from .models import Patient,MedicationEntry
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser  # custom user model import karo
from django.core.files.storage import FileSystemStorage



def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        qualification = request.POST['qualification']
        clinic_address = request.POST['clinic_address']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        profile_pic = request.FILES.get('profile_pic')

        # Username exists check
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # Password match check
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Create user
        user = CustomUser.objects.create_user(
            username=username,
            password=password1,
            name=name,
            qualification=qualification,
            clinic_address=clinic_address,
            phone=phone,
            profile_pic=profile_pic
        )
        user.save()
        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'home/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')  # ya aapka desired page
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')
    return render(request, 'home/login.html')

@login_required
def welcome(request):
    return render(request, 'home/welcome.html', {'username': request.user.username})

@login_required
def view_profile(request):
    user = request.user
    # user ek CustomUser instance hoga jisme signup ke waqt saari details hain
    return render(request, 'home/view_profile.html', {'user': user})

@login_required
def add_patient(request):
    # Receptionist only
    # if not request.user.groups.filter(name='Receptionist').exists():
    #     messages.error(request, "You are not authorized to add patients.")
    #     return redirect('welcome')

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.status = 'forwarded'  # Forward to doctor
            # You may want to assign a doctor here or later
            patient.save()
            messages.success(request, "Patient added and forwarded to doctor.")
            return redirect('add_patient')
    else:
        form = PatientForm()

    patients = Patient.objects.filter(status='forwarded', created_by=request.user)
    return render(request, 'home/add_patient.html', {'form': form, 'patients': patients})

@login_required
def doctor_forwarded_patients(request):
    # Doctor only
    if not request.user.groups.filter(name='Doctor').exists():
        messages.error(request, "You are not authorized to view this page.")
        return redirect('welcome')

    patients = Patient.objects.filter(status='forwarded', assigned_doctor=request.user)
    return render(request, 'home/doctor_forwarded_patients.html', {'patients': patients})

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def patient_detail_and_prescription(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=patient)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.status = 'done'
            
            # Save custom medications text (from textarea)
            custom_meds = request.POST.get('custom_medications', '').strip()
            prescription.medications = custom_meds
            
            prescription.save()

            # Clear previous medication entries for this patient
            patient.medication_entries.all().delete()

            # Collect all medications and dosages dynamically from form inputs
            medications = []
            index = 0
            while True:
                med_key = f'medications_{index}'
                dosage_key = f'dosages_{index}'
                med = request.POST.get(med_key)
                dosage = request.POST.get(dosage_key)
                if med is None:
                    break  # No more medications found, stop loop
                med = med.strip()
                if med:
                    dosage = dosage if dosage else 'once'  # Default dosage fallback
                    medications.append((med, dosage))
                index += 1

            # Save each medication and its dosage as MedicationEntry
            for med, dosage in medications:
                MedicationEntry.objects.create(patient=patient, medicine_name=med, dosage=dosage)

            messages.success(request, "Prescription saved and patient marked done.")
            return redirect('existing_patients')
    else:
        form = PrescriptionForm(instance=patient)

    return render(request, 'home/patient_prescription.html', {'patient': patient, 'form': form})



@login_required
def existing_patients(request):
    # Temporarily ignore group permissions
    patients = Patient.objects.filter(status='done', created_by=request.user)
    return render(request, 'home/existing_patients.html', {'patients': patients})




@login_required
def view_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'home/view_patient.html', {'patient': patient})

# edit view_patient.html file
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        patient.name = request.POST.get('name')
        patient.phone = request.POST.get('phone')
        patient.age = request.POST.get('age')
        patient.gender = request.POST.get('gender')
        patient.weight = request.POST.get('weight')
        patient.height = request.POST.get('height')
        patient.address = request.POST.get('address')
        patient.diagnosis = request.POST.get('diagnosis')
        patient.advice = request.POST.get('advice')
        patient.investigation = request.POST.get('investigation')
        patient.treatment_plan = request.POST.get('treatment_plan')
        patient.BP = request.POST.get("BP", patient.BP)
        patient.chief_complaints = request.POST.get("chief_complaints", patient.chief_complaints)
        patient.examination_findings = request.POST.get("examination_findings", patient.examination_findings)
        patient.medications = request.POST.get("medications", patient.medications)
        patient.save()
        return redirect('view_patient', patient_id=patient.id)

    return render(request, 'edit_patient.html', {'patient': patient})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def mark_done(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.status = 'done'
    patient.save()
    messages.success(request, f"Patient {patient.name} marked done.")
    return redirect('existing_patients')