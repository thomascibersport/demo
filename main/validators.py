from django.core.exceptions import ValidationError
import re

def validate_cyrillic(value):
    """
    Валидатор для проверки, что поле содержит только буквы кириллицы.
    """
    if not re.fullmatch(r'^[А-Яа-яЁё\s]+$', value):
        raise ValidationError('Поле должно содержать только буквы кириллицы и пробелы.')


class PasswordValidator:
    def validate(self, password, user=None):
        # Проверяем длину пароля
        if len(password) < 6:
            raise ValidationError("Пароль должен содержать не менее 6 символов.")

        # Проверяем наличие букв верхнего регистра
        if not any(char.isupper() for char in password):
            raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")

        # Проверяем наличие букв нижнего регистра
        if not any(char.islower() for char in password):
            raise ValidationError("Пароль должен содержать хотя бы одну строчную букву.")

        # Проверяем, что символы только английской раскладки
        if not re.match(r'^[A-Za-z0-9@./+/-/_]+$', password):
            raise ValidationError("Пароль должен содержать символы только английской раскладки.")

    def get_help_text(self):
        return (
            "Пароль должен содержать не менее 6 символов, включая буквы верхнего и нижнего регистра, "
            "и использовать только символы английской раскладки."
        )