from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Film, Genre, Ticket, Showtime, FilmImage


class FilmImageInline(admin.StackedInline):
    model = FilmImage
    extra = 1
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200" style="border-radius:6px;" />')
        return 'Изображение ещё не загружено'
    preview.short_description = 'Превью'


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display  = ['poster_preview', 'title', 'year', 'genre', 'country', 'rating', 'quality', 'duration', 'is_featured']
    list_display_links = ['title']
    list_filter   = ['genre', 'quality', 'country', 'is_featured', 'year']
    search_fields = ['title', 'genre', 'country']
    list_editable = ['rating', 'is_featured']
    readonly_fields = ['poster_preview']
    inlines = [FilmImageInline]

    fieldsets = (
        ('Основное', {
            'fields': ('title', 'year', 'slug', 'is_featured')
        }),
        ('Детали', {
            'fields': ('genre', 'country', 'quality', 'duration', 'price', 'rating')
        }),
        ('Медиа', {
            'fields': ('poster', 'poster_preview')
        }),
        ('Описание', {
            'fields': ('description',)
        }),
    )

    def poster_preview(self, obj):
        if obj.poster:
            return mark_safe(
                f'<img src="{obj.poster.url}" width="60" height="80" '
                f'style="object-fit:cover; border-radius:6px;" />'
            )
        return '—'
    poster_preview.short_description = 'Постер'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display  = ['genre']
    search_fields = ['genre']


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display   = ['film', 'date_time', 'hall_name', 'price']
    search_fields  = ['film__title']
    list_filter    = ['hall_name', 'date_time', 'film']
    date_hierarchy = 'date_time'


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display  = ['showtime', 'row_number', 'seat_number', 'is_bought']
    list_filter   = ['showtime', 'is_bought']
    search_fields = ['showtime__film__title']