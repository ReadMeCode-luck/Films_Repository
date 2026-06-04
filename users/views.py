from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ForgotPasswordForm
from .services import send_password_reset_email
from .models import CustomUser
from films.models import Favorite


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Вы успешно вошли.')
            return redirect('index')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Вы успешно зарегистрировались и вошли в аккаунт.')
            return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('index')


def forgot_password_view(request):
    """
    Принимает email из модального окна на странице логина.
    Если пользователь найден — отправляет письмо через services.py.
    Всегда редиректит обратно на логин с сообщением (чтобы не раскрывать,
    есть ли такой email в базе).
    """
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                send_password_reset_email(request, user)
            except CustomUser.DoesNotExist:
                pass  # не раскрываем, есть ли email в базе

        # Одно сообщение для обоих случаев — безопаснее
        messages.success(
            request,
            'Если этот email зарегистрирован, письмо со ссылкой уже в пути.'
        )
        return redirect('login')

    # GET-запрос на этот URL не нужен — редиректим на логин
    return redirect('login')


def profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    favorites = Favorite.objects.filter(user=profile_user).select_related('film').order_by('-created_at')
    favorites_count = favorites.count()
    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'favorites': favorites,
        'favorites_count': favorites_count,
    })