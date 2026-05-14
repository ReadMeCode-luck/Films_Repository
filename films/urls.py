from django.contrib import admin
from django.urls import path
from . import views
from .views import FilmList

urlpatterns = [
    path('', views.index, name='index'),
    path('api/films/', views.FilmList.as_view(), name='film-list'),
]