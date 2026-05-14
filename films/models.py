from django.db import models

class Film(models.Model):
    name = models.CharField(max_length=100, verbose_name = 'Фильм')
    year = models.IntegerField(verbose_name = 'Год')
    genre = models.CharField(max_length=100,verbose_name = 'Жанр')
    price = models.FloatField(verbose_name = 'Цена')
    description = models.TextField(verbose_name = 'Описание')


    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name= 'Жанр')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name