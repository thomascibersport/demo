from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser
from django.contrib.auth import get_user_model
import re
from django.core.exceptions import ValidationError

User = get_user_model()

# Валидатор для проверки кириллицы
def validate_cyrillic(value):
    if not re.match(r'^[А-ЯЁа-яё\s]+$', value):
        raise ValidationError("ФИО может содержать только буквы кириллицы.")

# Валидатор для проверки сложности пароля
def validate_password_strength(value):
    if len(value) < 6:
        raise ValidationError("Пароль должен содержать не менее 6 символов.")
    if not any(char.isupper() for char in value):
        raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")
    if not any(char.islower() for char in value):
        raise ValidationError("Пароль должен содержать хотя бы одну строчную букву.")
    if not re.match(r'^[A-Za-z0-9@./+/-/_]+$', value):
        raise ValidationError("Пароль должен содержать символы только английской раскладки.")

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[validate_password_strength],  # Подключаем валидатор
        label="Пароль"
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Подтвердите пароль")
    full_name = forms.CharField(validators=[validate_cyrillic], label="ФИО")
    
    # Изображение теперь обязательное для загрузки
    avatar = forms.ImageField(required=True, label="Аватар")  # Убираем 'required=False', теперь обязательное

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name', 'avatar']

    def clean(self):
        # Вызываем базовый метод clean
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Проверка совпадения паролей
        if password != confirm_password:
            raise ValidationError("Пароли не совпадают.")

        return cleaned_data
