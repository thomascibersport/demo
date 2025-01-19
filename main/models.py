from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.conf import settings

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


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


def validate_image(image):
    max_size = 2 * 1024 * 1024  # 2 MB
    if image.size > max_size:
        raise ValidationError("Размер изображения не должен превышать 2 MB.")

class UserAvatar(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='avatar')
    avatar = models.ImageField(upload_to='user_avatars/', blank=True, null=True)

    def __str__(self):
        return f"Avatar for {self.user.username}"