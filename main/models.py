from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass  # Используем только стандартные поля
class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='doctor_avatars/', blank=True, null=True)
    working_hours = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.specialty})"


class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('past', 'Past')])


