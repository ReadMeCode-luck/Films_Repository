from django.db import models
from autoslug import AutoSlugField
from django.utils.safestring import mark_safe


class Film(models.Model):
    QUALITY_CHOICES = [
        ('HD', 'HD'),
        ('Full HD', 'Full HD'),
        ('4K', '4K'),
        ('CAM', 'CAM'),
    ]

    title       = models.CharField(max_length=200, verbose_name='Название')
    year        = models.IntegerField(verbose_name='Год')
    genre       = models.CharField(max_length=200, verbose_name='Жанр')
    country     = models.CharField(max_length=100, verbose_name='Страна', blank=True, default='')
    description = models.TextField(verbose_name='Описание', blank=True)
    rating      = models.DecimalField(
        max_digits=3, decimal_places=1,
        verbose_name='Рейтинг', default=0.0,
        help_text='От 0.0 до 10.0'
    )
    duration    = models.PositiveIntegerField(
        verbose_name='Длительность (мин)', default=0
    )
    quality     = models.CharField(
        max_length=20, choices=QUALITY_CHOICES,
        default='HD', verbose_name='Качество'
    )
    price       = models.FloatField(verbose_name='Цена', default=0)
    poster      = models.ImageField(
        upload_to='posters/', verbose_name='Постер',
        blank=True, null=True
    )
    is_featured = models.BooleanField(default=False, verbose_name='Показывать на главной')

    slug = AutoSlugField(
        populate_from='title',
        unique_with=['year'],
        always_update=True,
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['-rating']

    def __str__(self):
        return f'{self.title} ({self.year})'

    def duration_display(self):
        """Возвращает строку вида '2ч 36м'."""
        h = self.duration // 60
        m = self.duration % 60
        return f'{h}ч {m}м' if h else f'{m}м'


class FilmImage(models.Model):
    film  = models.ForeignKey(Film, related_name='images', on_delete=models.CASCADE, verbose_name='Фильм')
    image = models.ImageField('Изображение/Кадр', upload_to='movies/')

    class Meta:
        verbose_name = 'Изображение фильма'
        verbose_name_plural = 'Изображения фильма'


class Genre(models.Model):
    genre = models.CharField(max_length=100, verbose_name='Жанр')
    slug  = AutoSlugField(populate_from='genre', unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.genre


class Showtime(models.Model):
    film      = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name='Фильм')
    date_time = models.DateTimeField(verbose_name='Дата и время сеанса')
    hall_name = models.CharField(max_length=50, verbose_name='Зал')
    price     = models.FloatField(verbose_name='Цена билета на этот сеанс')

    class Meta:
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеансы'

    def __str__(self):
        return f'{self.film.title} — {self.date_time.strftime("%d.%m.%Y %H:%M")} ({self.hall_name})'


class Ticket(models.Model):
    showtime   = models.ForeignKey(Showtime, on_delete=models.CASCADE, verbose_name='Сеанс')
    seat_number = models.IntegerField(verbose_name='Место')
    row_number  = models.IntegerField(verbose_name='Ряд')
    is_bought   = models.BooleanField(default=False, verbose_name='Куплен')

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
        unique_together = ('showtime', 'row_number', 'seat_number')