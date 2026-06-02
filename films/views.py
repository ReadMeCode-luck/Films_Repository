from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.generics import ListAPIView
from django.template.context_processors import csrf
from django.db.models import Q
from .models import Film, Genre, Slider, FeaturedFilm, FeaturedCartoon, COUNTRY_CHOICES

YEAR_MIN = 1895
YEAR_MAX = 2026


def _get_genre_choices():
    """Жанры из Genre модели в виде списка (val, label) для шаблонов."""
    return [(g.genre, g.genre) for g in Genre.objects.all().order_by('genre')]


def index(request):
    sliders           = Slider.objects.filter(is_active=True)
    featured_films    = FeaturedFilm.objects.select_related('film').order_by('position')[:5]
    featured_cartoons = FeaturedCartoon.objects.select_related('film').order_by('position')[:5]
    years = list(range(YEAR_MAX, YEAR_MIN - 1, -1))
    context = {
        'sliders':            sliders,
        'featured_films':     featured_films,
        'featured_cartoons':  featured_cartoons,
        'genre_choices':      _get_genre_choices(),
        'country_choices':    COUNTRY_CHOICES,
        'years':              years,
    }
    return render(request, 'home.html', context)


def _apply_filters(films, request):
    """Общая логика фильтрации для фильмов и мультфильмов."""
    genre_filter   = request.GET.get('genre', '')
    country_filter = request.GET.get('country', '')
    quality_filter = request.GET.get('quality', '')
    year_from      = request.GET.get('year_from', '')
    year_to        = request.GET.get('year_to', '')
    sort_by        = request.GET.get('sort', '-rating')
    search_query   = request.GET.get('q', '')

    if genre_filter:
        films = films.filter(genre=genre_filter)
    if country_filter:
        films = films.filter(country=country_filter)
    if quality_filter:
        films = films.filter(quality=quality_filter)
    if year_from.isdigit():
        films = films.filter(year__gte=int(year_from))
    if year_to.isdigit():
        films = films.filter(year__lte=int(year_to))
    if search_query:
        films = films.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    allowed_sort = ['-rating', 'rating', '-year', 'year', 'title', '-title']
    if sort_by in allowed_sort:
        films = films.order_by(sort_by)

    return films, {
        'genre_filter':   genre_filter,
        'country_filter': country_filter,
        'quality_filter': quality_filter,
        'year_from':      year_from,
        'year_to':        year_to,
        'sort_by':        sort_by,
        'search_query':   search_query,
    }


def films_page(request):
    """Страница «Фильмы» с фильтрацией и поиском."""
    films = Film.objects.filter(is_cartoon=False)
    films, filter_ctx = _apply_filters(films, request)

    years = list(range(YEAR_MAX, YEAR_MIN - 1, -1))
    context = {
        'films':         films,
        'genre_choices':    _get_genre_choices(),
        'country_choices':  COUNTRY_CHOICES,
        'years':         years,
        'total_count':   films.count(),
        'page_type':     'films',
        **filter_ctx,
    }
    return render(request, 'films.html', context)


def cartoons_page(request):
    """Страница «Мультфильмы» с фильтрацией и поиском."""
    films = Film.objects.filter(is_cartoon=True)
    films, filter_ctx = _apply_filters(films, request)

    featured_cartoons = FeaturedCartoon.objects.select_related('film').order_by('position')[:5]
    years = list(range(YEAR_MAX, YEAR_MIN - 1, -1))
    context = {
        'films':              films,
        'genre_choices':      _get_genre_choices(),
        'country_choices':    COUNTRY_CHOICES,
        'years':              years,
        'total_count':        films.count(),
        'page_type':          'cartoons',
        'featured_cartoons':  featured_cartoons,
        **filter_ctx,
    }
    return render(request, 'cartoons.html', context)


def film_detail(request, slug):
    film = get_object_or_404(Film, slug=slug)
    return render(request, 'film_detail.html', {'film': film})


class FilmList(ListAPIView):
    queryset = Film.objects.all()


def entrance(request):
    return redirect('login')


def any_request(request):
    context = {}
    context.update(csrf(request))
    return render(request, 'any_request.html', context)


# ── Обработчики ошибок ──────────────────────────────────────────────────────

def e_handler400(request, exception):
    return render(request, 'errors/400.html', status=400)

def csrf_failure(request, reason=''):
    return render(request, 'errors/403.html', status=403)

def e_handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def e_handler500(request):
    return render(request, 'errors/500.html', status=500)