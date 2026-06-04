from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListAPIView
from django.template.context_processors import csrf
from django.db.models import Q
from collections import defaultdict
from .models import Film, Genre, SliderItem, BannerItem, FeaturedFilm, FeaturedCartoon, Showtime, Ticket, Favorite, COUNTRY_CHOICES

YEAR_MIN = 1895
YEAR_MAX = 2026


def _get_genre_choices():
    """Жанры из Genre модели в виде списка (val, label) для шаблонов."""
    return [(g.genre, g.genre) for g in Genre.objects.all().order_by('genre')]


def index(request):
    slider_items      = SliderItem.objects.select_related('film').order_by('order')
    banner_item       = BannerItem.objects.select_related('film').first()
    featured_films    = FeaturedFilm.objects.select_related('film').order_by('position')[:5]
    featured_cartoons = FeaturedCartoon.objects.select_related('film').order_by('position')[:5]
    years = list(range(YEAR_MAX, YEAR_MIN - 1, -1))
    context = {
        'slider_items':       slider_items,
        'banner_item':        banner_item,
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
        films = films.filter(title__istartswith=search_query)

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
    showtimes = Showtime.objects.filter(film=film).order_by('date_time')

    # Group showtimes by date
    grouped = defaultdict(list)
    for st in showtimes:
        date_key = st.date_time.date()
        grouped[date_key].append(st)

    showtimes_by_date = [
        {'date': date, 'showtimes': items}
        for date, items in sorted(grouped.items())
    ]

    is_favorited = (
        request.user.is_authenticated
        and Favorite.objects.filter(user=request.user, film=film).exists()
    )

    return render(request, 'film_detail.html', {
        'film': film,
        'showtimes_by_date': showtimes_by_date,
        'is_favorited': is_favorited,
    })


@login_required
@require_POST
def toggle_favorite(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    fav, created = Favorite.objects.get_or_create(user=request.user, film=film)
    if not created:
        fav.delete()
        favorited = False
    else:
        favorited = True
    return JsonResponse({'favorited': favorited})


@login_required
@require_POST
def remove_favorite(request, film_id):
    """Удалить конкретный фильм из избранного."""
    film = get_object_or_404(Film, pk=film_id)
    Favorite.objects.filter(user=request.user, film=film).delete()
    return JsonResponse({'removed': True})


@login_required
@require_POST
def clear_all_favorites(request):
    """Удалить всё избранное текущего пользователя."""
    Favorite.objects.filter(user=request.user).delete()
    return JsonResponse({'cleared': True})


def seat_selection(request, showtime_id):
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    tickets = Ticket.objects.filter(showtime=showtime).order_by('row_number', 'seat_number')

    # Build row-based grid
    rows = defaultdict(list)
    for t in tickets:
        rows[t.row_number].append(t)
    seat_grid = [{'row': row, 'seats': seats} for row, seats in sorted(rows.items())]

    return render(request, 'seat_selection.html', {
        'showtime': showtime,
        'seat_grid': seat_grid,
    })


@require_POST
def book_seats(request, showtime_id):
    """Mark selected seats as bought and show confirmation."""
    from django.utils import timezone
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    seat_ids = request.POST.getlist('seats')  # list of ticket PKs

    booked = []
    for tid in seat_ids:
        try:
            ticket = Ticket.objects.get(pk=int(tid), showtime=showtime, is_bought=False)
            ticket.is_bought = True
            ticket.bought_at = timezone.now()
            if request.user.is_authenticated:
                ticket.user = request.user
            ticket.save()
            booked.append(ticket)
        except (Ticket.DoesNotExist, ValueError):
            pass

    total = sum(showtime.price for _ in booked)
    return render(request, 'booking_confirmation.html', {
        'showtime': showtime,
        'booked': booked,
        'total': total,
    })


@login_required
def my_tickets(request):
    tickets = (
        Ticket.objects
        .filter(user=request.user, is_bought=True)
        .select_related('showtime__film')
        .order_by('-bought_at')
    )
    return render(request, 'my_tickets.html', {'tickets': tickets})


class FilmList(ListAPIView):
    queryset = Film.objects.all()


def live_search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if len(query) >= 2:
        films = Film.objects.filter(title__istartswith=query).values(
            'id', 'title', 'year', 'rating', 'slug'
        )[:8]
        results = list(films)
    return JsonResponse({'results': results})


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
