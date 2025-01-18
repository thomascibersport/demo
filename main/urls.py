from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('appointments/create/', views.create_appointment, name='create_appointment'),
    path('appointments/', views.appointments_list, name='appointments_list'),
    path('appointments/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('search/doctors/', views.search_doctors, name='search_doctors'),
    path('import/services/', views.import_services, name='import_services'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)