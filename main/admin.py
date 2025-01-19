from django.contrib import admin
from .models import Service
from .models import Doctor, Appointment, CustomUser

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'working_hours')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor', 'date', 'status')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Отображаемые поля в списке услуг
    search_fields = ('name', 'description')  # Поля для поиска

