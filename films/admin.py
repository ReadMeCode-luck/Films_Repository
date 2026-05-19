from django.contrib import admin
from .models import Film, Genre, Ticket, Showtime, FilmImage
from django.utils.safestring import mark_safe

class FilmImageInline(admin.StackedInline):
    model = FilmImage
    extra = 3
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200" style="border-radius: 5px;" />')
        return "Изображение еще не загружено"

    preview.short_description = "Превью кадра"

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    # Настройки отображения списка фильмов
    list_display = ['title', 'price', 'genre', 'year']
    list_filter = ['price']
    search_fields = ['title', 'genre', 'year']

    inlines = [FilmImageInline]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre']
    list_filter = ['genre']
    search_fields = ['genre']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['showtime', 'row_number', 'seat_number', 'is_bought']
    list_filter = ['showtime']
    search_fields = ['showtime__film__title']

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ['film', 'date_time', 'hall_name', 'price']
    search_fields = ['film__title']
    list_filter = ['hall_name', 'date_time', 'film']
    date_hierarchy = 'date_time'

def __str__(self):
    formatted_time = self.date_time.strftime('%d.%m.%Y %H:%M')
    return f"{self.film.name} — {formatted_time} ({self.hall_name})"


