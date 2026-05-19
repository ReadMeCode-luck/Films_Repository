from django.db import models
from autoslug import AutoSlugField
from django.utils.text import slugify
from django.utils.safestring import mark_safe

class Film(models.Model):
    title = models.CharField(max_length=100, verbose_name='Фильм')
    year = models.IntegerField(verbose_name='Год')
    genre = models.CharField(max_length=100, verbose_name='Жанр')
    price = models.FloatField(verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')

    slug = AutoSlugField(
        populate_from='title',
        unique_with=['year'],
        always_update=True,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title

class FilmImage(models.Model):
    film = models.ForeignKey(
        Film,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Фильм"
    )
    image = models.ImageField("Изображение/Кадр", upload_to="movies/")

    class Meta:
        verbose_name = "Изображение фильма"
        verbose_name_plural = "Изображения фильма"


class Genre(models.Model):
    genre = models.CharField(max_length=100, verbose_name='Жанр')

    slug = AutoSlugField(
        populate_from='genre',
        unique=True,
        null = True,
        blank = True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.genre

class Showtime(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name='Фильм')
    date_time = models.DateTimeField(verbose_name='Дата и время сеанса')
    hall_name = models.CharField(max_length=50, verbose_name='Зал')
    price = models.FloatField(verbose_name='Цена билета на этот сеанс')

    class Meta:
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеансы'

class Ticket(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, verbose_name='Сеанс')
    seat_number = models.IntegerField(verbose_name='Место')
    row_number = models.IntegerField(verbose_name='Ряд')
    is_bought = models.BooleanField(default=False, verbose_name='Куплен')

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
        unique_together = ('showtime', 'row_number', 'seat_number')