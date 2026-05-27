from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import re
from .models import CustomUser


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError('Неверный логин или пароль')

            self.user_cache = user

        return cleaned_data

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(label='ФИО', max_length=150)
    phone = forms.CharField(label='Телефон', max_length=20)
    email = forms.EmailField(label='Email')

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'phone', 'email', 'password1', 'password2')
        labels = {
           'username': 'Логин'
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not re.fullmatch(r'[A-Za-z0-9]+', username):
            raise ValidationError('Логин должен содержать только латинские буквы и цифры')

        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует')

        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')

        if not re.fullmatch(r'[А-Яа-яЁё\s]+', full_name):
            raise ValidationError('ФИО должно содержать только кириллицу и пробелы')

        return full_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        clean_digits = re.sub(r'[^\d+]', '', phone)

        if not re.fullmatch(r'(?:\+7|7|8)\d{10}', clean_digits):
            raise ValidationError('Неверный формат номера. Пример: +7 (999) 123-45-67 или 8 (999) 123-45-67')

        if clean_digits.startswith('8'):
            clean_digits = '+7' + clean_digits[1:]
        elif clean_digits.startswith('7'):
            clean_digits = '+' + clean_digits

        if CustomUser.objects.filter(phone=clean_digits).exclude(
                pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError('Пользователь с таким телефоном уже существует')

        formatted_phone = f"{clean_digits[0:2]} ({clean_digits[2:5]}) {clean_digits[5:8]}-{clean_digits[8:10]}-{clean_digits[10:12]}"
        return formatted_phone
