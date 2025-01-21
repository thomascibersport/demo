from django.contrib import admin
from .models import Service, Doctor, Appointment, CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()  # Получаем модель пользователя

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'working_hours')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor', 'date', 'status')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Отображаемые поля в списке услуг
    search_fields = ('name', 'description')  # Поля для поиска

# Проверяем, зарегистрирована ли модель CustomUser
try:
    admin.site.unregister(User)  # Удаляем стандартную регистрацию пользователя
except admin.sites.NotRegistered:
    pass  # Если модель не была зарегистрирована, просто продолжаем

# Регистрация модели CustomUser с кастомной админкой
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'full_name', 'is_staff')  # Добавляем ФИО в список
    search_fields = ('username', 'email', 'first_name', 'last_name')  # Поиск по имени и фамилии

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"  # Форматируем ФИО
    full_name.short_description = 'ФИО'  # Заголовок столбца

admin.site.register(User, CustomUserAdmin)
