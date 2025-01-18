# main/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
from datetime import timedelta
from .models import Doctor
from .models import Appointment
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Service

def index(request):
    return render(request, 'main/index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/admin')  # Панель администратора
            return redirect('/dashboard')  # Личный кабинет
        else:
            return render(request, 'main/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'main/login.html')

@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')

def user_logout(request):
    logout(request)
    return redirect('login')
@staff_member_required
def admin_dashboard(request):
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all()
    return render(request, 'main/admin_dashboard.html', {'doctors': doctors, 'appointments': appointments})

@staff_member_required
def add_doctor(request):
    if request.method == 'POST':
        name = request.POST['name']
        specialty = request.POST['specialty']
        working_hours = request.POST['working_hours']
        avatar = request.FILES.get('avatar')
        Doctor.objects.create(name=name, specialty=specialty, working_hours=working_hours, avatar=avatar)
        return redirect('admin_dashboard')
    return render(request, 'main/add_doctor.html')





def create_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST['doctor']
        date = request.POST['date']
        Appointment.objects.create(
            user=request.user,
            doctor_id=doctor_id,
            date=date,
            status='active'
        )
        return redirect('appointments_list')

    doctors = Doctor.objects.all()
    return render(request, 'main/create_appointment.html', {'doctors': doctors})
def appointments_list(request):
    appointments = Appointment.objects.filter(user=request.user)
    active_appointments = appointments.filter(date__gte=now())
    past_appointments = appointments.filter(date__lt=now())

    return render(request, 'main/appointments_list.html', {
        'active_appointments': active_appointments,
        'past_appointments': past_appointments,
    })
def cancel_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id, user=request.user)
    # Проверка, можно ли отменить запись
    if appointment.date <= now() + timedelta(days=1):
        messages.error(request, "Вы не можете отменить запись менее чем за 1 день до приёма.")
    else:
        appointment.delete()
        messages.success(request, "Запись успешно отменена.")
    return redirect('appointments_list') 

@staff_member_required
def add_doctor(request):
    if request.method == 'POST':
        name = request.POST['name']
        specialty = request.POST['specialty']
        working_hours = request.POST['working_hours']
        avatar = request.FILES.get('avatar')
        Doctor.objects.create(name=name, specialty=specialty, working_hours=working_hours, avatar=avatar)
        return redirect('admin_dashboard')
    return render(request, 'main/add_doctor.html')
def search_doctors(request):
    query = request.GET.get('q', '').strip()  # Получаем текст поиска
    if query:
        results = Doctor.objects.filter(name__icontains=query)[:10]
        data = [
            {
                'id': doctor.id,
                'name': doctor.name,
                'specialty': doctor.specialty,
                'working_hours': doctor.working_hours,
                'avatar': doctor.avatar.url if doctor.avatar else None
            }
            for doctor in results
        ]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)
def doctors_list(request):
    doctors = Doctor.objects.all()  # Получаем всех врачей
    paginator = Paginator(doctors, 12)  # 5 врачей на страницу
    page_number = request.GET.get('page')  # Номер текущей страницы
    page_obj = paginator.get_page(page_number)  # Получаем объекты для текущей страницы
    return render(request, 'main/doctors_list.html', {'page_obj': page_obj})

def import_services(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        try:
            tree = ET.parse(file)
            root = tree.getroot()

            for service in root.findall('service'):
                name = service.find('name').text
                description = service.find('description').text

                # Создаём или обновляем запись в базе
                Service.objects.update_or_create(name=name, defaults={'description': description})

            messages.success(request, "Услуги успешно импортированы.")
        except Exception as e:
            messages.error(request, f"Ошибка при импорте файла: {e}")

        return redirect('import_services')

    return render(request, 'main/import_services.html')

