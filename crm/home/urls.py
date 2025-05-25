from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('welcome/', views.welcome, name='welcome'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('existing-patients/', views.existing_patients, name='existing_patients'),
    path('mark-done/<int:patient_id>/', views.mark_done, name='mark_done'),
    path('add-prescription/<int:patient_id>/', views.patient_detail_and_prescription, name='add_prescription'),
    path('profile/', views.view_profile, name='view_profile'),

    # Ye wali line add karo:
    path('doctor/patients/', views.doctor_forwarded_patients, name='doctor_forwarded_patients'),
    #to view patient 
    path('patient/<int:patient_id>/', views.view_patient, name='view_patient'),
    path('patient/<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)