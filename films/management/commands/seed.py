"""
python manage.py seed                   — заполнить (10 фильмов, 5 мультфильмов, слайдер, баннер)
python manage.py seed --films 20        — указать количество фильмов
python manage.py seed --clear           — очистить и заполнить заново
python manage.py seed --clear-only      — только очистить
python manage.py seed --no-images       — без скачивания картинок
"""

import random
import urllib.request
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone
from faker import Faker

from films.models import (
    Film, Genre, Showtime, Ticket,
    SliderItem, BannerItem,
    FeaturedFilm, FeaturedCartoon,
    COUNTRY_CHOICES,
)

fake = Faker('ru_RU')

GENRES = [
    'Комедия', 'Драма', 'Боевик', 'Хоррор', 'Научная фантастика',
    'Фэнтези', 'Вестерн', 'Детектив', 'Мюзикл', 'Документальный',
]

HALLS = [
    ('Зал 1 (Стандарт)', 8, 12, 400),
    ('Зал 2 (Комфорт)',  7, 10, 600),
    ('VIP 1 (Премиум)',  5,  8, 1200),
    ('VIP Лофт',         4,  6, 2500),
]

AGE_RATINGS = ['0+', '6+', '12+', '16+', '18+']
QUALITIES   = ['HD', 'Full HD', '4K']


# ── Загрузка изображений ──────────────────────────────────────────────────────

def _fetch(url: str) -> bytes | None:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.read()
    except Exception:
        return None


def _poster(seed: int) -> ContentFile | None:
    data = _fetch(f'https://picsum.photos/seed/{seed}/400/600')
    return ContentFile(data, name=f'poster_{seed}.jpg') if data else None


def _wide(seed: int) -> ContentFile | None:
    data = _fetch(f'https://picsum.photos/seed/{seed}/1280/720')
    return ContentFile(data, name=f'wide_{seed}.jpg') if data else None


# ── Создание объектов ─────────────────────────────────────────────────────────

def _make_film(is_cartoon=False, fetch_images=True) -> Film:
    film = Film(
        title=fake.catch_phrase()[:50],
        year=random.randint(2000, 2026),
        genre=random.choice(GENRES),
        country=random.choice([c[0] for c in COUNTRY_CHOICES]),
        description=fake.text(max_nb_chars=400),
        rating=round(random.uniform(5.0, 9.5), 1),
        duration=random.randint(70, 180),
        quality=random.choice(QUALITIES),
        price=random.choice([200, 300, 400, 500, 600]),
        age_rating=random.choice(AGE_RATINGS),
        is_cartoon=is_cartoon,
        is_featured=False,
    )

    if fetch_images:
        img = _poster(random.randint(1, 9999))
        if img:
            # ПРЯМОЕ ПРИСВОЕНИЕ: файл сохранится автоматически вместе с моделью
            film.poster = img

    film.save()
    return film

def _make_showtime(film: Film):
    hall_name, rows, seats, price = random.choice(HALLS)
    dt = timezone.now() + timezone.timedelta(
        days=random.randint(0, 14),
        hours=random.randint(10, 22),
        minutes=random.choice([0, 15, 30, 45]),
    )
    st = Showtime.objects.create(
        film=film, date_time=dt,
        hall_name=hall_name, price=price,
        rows=rows, seats_per_row=seats,
    )
    tickets = [
        Ticket(showtime=st, row_number=r, seat_number=s,
               is_bought=random.random() < 0.3)
        for r in range(1, rows + 1)
        for s in range(1, seats + 1)
    ]
    Ticket.objects.bulk_create(tickets, ignore_conflicts=True)


# ── Команда ───────────────────────────────────────────────────────────────────

class Command(BaseCommand):
    help = 'Заполняет БД тестовыми данными через Faker.'

    def add_arguments(self, parser):
        parser.add_argument('--films',    type=int, default=10)
        parser.add_argument('--cartoons', type=int, default=5)
        parser.add_argument('--no-images', action='store_true')
        parser.add_argument('--clear',     action='store_true')
        parser.add_argument('--clear-only', action='store_true')

    def handle(self, *args, **options):
        fetch = not options['no_images']

        if options['clear'] or options['clear_only']:
            self._clear()
            if options['clear_only']:
                self.stdout.write(self.style.SUCCESS('✓ Данные очищены.'))
                return

        # Жанры
        self.stdout.write('  → Жанры...')
        for g in GENRES:
            Genre.objects.get_or_create(genre=g)

        # Фильмы
        n_films = options['films']
        self.stdout.write(f'  → {n_films} фильмов...')
        films = [_make_film(is_cartoon=False, fetch_images=fetch) for _ in range(n_films)]

        # Мультфильмы
        n_cartoons = options['cartoons']
        self.stdout.write(f'  → {n_cartoons} мультфильмов...')
        cartoons = [_make_film(is_cartoon=True, fetch_images=fetch) for _ in range(n_cartoons)]

        # Сеансы
        self.stdout.write('  → Сеансы и места...')
        for film in films + cartoons:
            for _ in range(random.randint(2, 3)):
                _make_showtime(film)

        # FeaturedFilm — до 5 позиций
        self.stdout.write('  → Рекомендуемые фильмы...')
        used_pos = set(FeaturedFilm.objects.values_list('position', flat=True))
        for pos, film in enumerate(random.sample(films, min(5, len(films))), 1):
            if pos not in used_pos:
                FeaturedFilm.objects.get_or_create(film=film, defaults={'position': pos})

        # FeaturedCartoon — до 5 позиций
        used_pos = set(FeaturedCartoon.objects.values_list('position', flat=True))
        for pos, cartoon in enumerate(random.sample(cartoons, min(5, len(cartoons))), 1):
            if pos not in used_pos:
                FeaturedCartoon.objects.get_or_create(film=cartoon, defaults={'position': pos})

        # SliderItem — 4 фильма в карусели
        self.stdout.write('  → Слайдер (герой-карусель)...')
        used_orders = set(SliderItem.objects.values_list('order', flat=True))
        slider_candidates = [f for f in films if not SliderItem.objects.filter(film=f).exists()]
        for order, film in enumerate(random.sample(slider_candidates, min(4, len(slider_candidates))), 1):
            if order not in used_orders:
                SliderItem.objects.create(film=film, order=order)

        # BannerItem — один промо-баннер
        self.stdout.write('  → Промо-баннер...')
        if not BannerItem.objects.exists():
            slider_film_ids = set(SliderItem.objects.values_list('film_id', flat=True))
            banner_candidates = [f for f in films if f.id not in slider_film_ids]
            if not banner_candidates:
                banner_candidates = films
            if banner_candidates:
                BannerItem.objects.create(film=random.choice(banner_candidates))

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Готово! {n_films} фильмов, {n_cartoons} мультфильмов, '
            f'{SliderItem.objects.count()} слайдов, '
            f'{BannerItem.objects.count()} баннер.'
        ))
        if not fetch:
            self.stdout.write(self.style.WARNING(
                '  (картинки не загружались — запустите без --no-images)'
            ))

    def _clear(self):
        self.stdout.write('  → Очищаем...')
        BannerItem.objects.all().delete()
        SliderItem.objects.all().delete()
        FeaturedFilm.objects.all().delete()
        FeaturedCartoon.objects.all().delete()
        Ticket.objects.all().delete()
        Showtime.objects.all().delete()
        Film.objects.all().delete()
        self.stdout.write('  → Готово.')
