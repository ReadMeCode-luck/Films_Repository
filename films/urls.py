from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('films/', views.films_page, name='films'),
    path('films/<slug:slug>/', views.film_detail, name='film_detail'),
    path('profile/', include('users.urls')),
    path('api/films/', views.FilmList.as_view(), name='film-list'),
    path('admin/', admin.site.urls),
    path('entrance/', views.entrance, name='entrance'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'films.views.e_handler400'
handler404 = 'films.views.e_handler404'
handler403 = 'films.views.csrf_failure'
handler500 = 'films.views.e_handler500'