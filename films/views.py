from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.generics import ListAPIView
from django.template.context_processors import csrf
from django.db.models import Q
from .models import Film, Genre


def index(request):
    films = Film.objects.all()
    context = {'films': films}
    return render(request, 'home.html', context)


def films_page(request):
    """Страница «Фильмы» с фильтрацией и поиском."""
    films = Film.objects.all()

    # --- фильтры ---
    genre_filter   = request.GET.get('genre', '')
    country_filter = request.GET.get('country', '')
    quality_filter = request.GET.get('quality', '')
    sort_by        = request.GET.get('sort', '-rating')
    search_query   = request.GET.get('q', '')

    if genre_filter:
        films = films.filter(genre__icontains=genre_filter)
    if country_filter:
        films = films.filter(country__icontains=country_filter)
    if quality_filter:
        films = films.filter(quality=quality_filter)
    if search_query:
        films = films.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    allowed_sort = ['-rating', 'rating', '-year', 'year', 'title', '-title']
    if sort_by in allowed_sort:
        films = films.order_by(sort_by)

    genres    = Genre.objects.all()
    countries = Film.objects.exclude(country='').values_list('country', flat=True).distinct()

    context = {
        'films':          films,
        'genres':         genres,
        'countries':      countries,
        'genre_filter':   genre_filter,
        'country_filter': country_filter,
        'quality_filter': quality_filter,
        'sort_by':        sort_by,
        'search_query':   search_query,
        'total_count':    films.count(),
    }
    return render(request, 'films.html', context)


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