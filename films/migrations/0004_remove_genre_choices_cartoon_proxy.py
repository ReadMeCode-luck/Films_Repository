from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_add_slider_featured_choices'),
    ]

    operations = [
        # Убираем choices= с Film.genre — теперь жанр берётся из Genre модели
        migrations.AlterField(
            model_name='film',
            name='genre',
            field=models.CharField(
                blank=True,
                default='',
                max_length=100,
                verbose_name='Жанр',
            ),
        ),

        # Прокси-модель CartoonFilm для отдельной секции «Мультфильмы» в админке
        migrations.CreateModel(
            name='CartoonFilm',
            fields=[],
            options={
                'verbose_name': 'Мультфильм',
                'verbose_name_plural': 'Мультфильмы',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('films.film',),
        ),
    ]
