from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
from .models import Film, CartoonFilm, Genre, Ticket, Showtime, FilmImage, Slider, FeaturedFilm, FeaturedCartoon

# Убираем ненужный раздел «Сайты» из админки
try:
    admin.site.unregister(Site)
except admin.sites.NotRegistered:
    pass


# ── Форма Film с динамическим выбором жанра из Genre модели ─────────────────

class FilmAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        genre_qs = Genre.objects.all().order_by('genre')
        genre_choices = [('', '— Не выбрано —')] + [(g.genre, g.genre) for g in genre_qs]
        self.fields['genre'] = forms.ChoiceField(
            choices=genre_choices,
            required=False,
            label='Жанр',
        )
        self.fields['genre'].widget.attrs.update({'class': 'select2'})

    class Meta:
        model = Film
        fields = '__all__'


# ── Инлайны ─────────────────────────────────────────────────────────────────

class FilmImageInline(admin.StackedInline):
    model = FilmImage
    extra = 1
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200" style="border-radius:6px;" />')
        return 'Изображение ещё не загружено'
    preview.short_description = 'Превью'


# ── Базовый класс AdminFilm ──────────────────────────────────────────────────

class BaseFilmAdmin(admin.ModelAdmin):
    form = FilmAdminForm
    list_display_links = ['title']
    list_filter   = ['genre', 'quality', 'country', 'is_featured', 'year']
    search_fields = ['title', 'genre', 'country']
    readonly_fields = ['poster_preview']
    inlines = [FilmImageInline]

    fieldsets = (
        ('Основное', {
            'fields': ('title', 'year', 'is_featured')
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


# ── FilmAdmin (только фильмы, is_cartoon=False) ──────────────────────────────

@admin.register(Film)
class FilmAdmin(BaseFilmAdmin):
    list_display  = ['poster_preview', 'title', 'year', 'genre', 'country',
                     'rating', 'quality', 'duration', 'is_featured', 'is_cartoon']
    list_editable = ['rating', 'is_featured', 'is_cartoon']

    fieldsets = (
        ('Основное', {
            'fields': ('title', 'year', 'is_featured', 'is_cartoon')
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

    def get_queryset(self, request):
        return super().get_queryset(request)


# ── CartoonAdmin (только мультфильмы) ────────────────────────────────────────

@admin.register(CartoonFilm)
class CartoonAdmin(BaseFilmAdmin):
    list_display  = ['poster_preview', 'title', 'year', 'genre', 'country',
                     'rating', 'quality', 'duration', 'is_featured']
    list_editable = ['rating', 'is_featured']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_cartoon=True)

    def save_model(self, request, obj, form, change):
        obj.is_cartoon = True
        super().save_model(request, obj, form, change)


# ── Остальные модели ─────────────────────────────────────────────────────────

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display  = ['genre', 'slug']
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


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display  = ['slide_preview', 'title', 'genre', 'duration', 'rating', 'order', 'is_active']
    list_display_links = ['title']
    list_editable = ['order', 'is_active']
    readonly_fields = ['slide_preview']

    fieldsets = (
        ('Контент', {
            'fields': ('title', 'description', 'genre', 'duration', 'rating')
        }),
        ('Изображение', {
            'fields': ('image', 'slide_preview')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
    )

    def slide_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="160" height="90" '
                f'style="object-fit:cover; border-radius:6px;" />'
            )
        return '—'
    slide_preview.short_description = 'Превью'


@admin.register(FeaturedFilm)
class FeaturedFilmAdmin(admin.ModelAdmin):
    list_display  = ['position', 'film_poster', 'film']
    list_display_links = ['film']
    ordering = ['position']

    def film_poster(self, obj):
        if obj.film.poster:
            return mark_safe(
                f'<img src="{obj.film.poster.url}" width="40" height="55" '
                f'style="object-fit:cover; border-radius:4px;" />'
            )
        return '—'
    film_poster.short_description = 'Постер'


@admin.register(FeaturedCartoon)
class FeaturedCartoonAdmin(admin.ModelAdmin):
    list_display  = ['position', 'film_poster', 'film']
    list_display_links = ['film']
    ordering = ['position']

    def film_poster(self, obj):
        if obj.film.poster:
            return mark_safe(
                f'<img src="{obj.film.poster.url}" width="40" height="55" '
                f'style="object-fit:cover; border-radius:4px;" />'
            )
        return '—'
    film_poster.short_description = 'Постер'
