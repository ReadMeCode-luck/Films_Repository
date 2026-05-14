from django.contrib import admin
from .models import Film, Genre


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['name','price']
    list_filter = ['price']
    search_fields = ['name']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
