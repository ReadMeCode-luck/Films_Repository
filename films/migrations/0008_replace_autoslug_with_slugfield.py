from django.db import migrations, models
from django.utils.text import slugify


def fill_film_slugs(apps, schema_editor):
    Film = apps.get_model('films', 'Film')
    used = set()
    for film in Film.objects.order_by('id'):
        base = slugify(film.title, allow_unicode=True) or f'film-{film.pk}'
        # Обрезаем до 200 символов чтобы гарантированно влезть в varchar(220)
        base = base[:200]
        slug = base
        n = 1
        while slug in used:
            slug = f'{base}-{n}'
            n += 1
        Film.objects.filter(pk=film.pk).update(slug=slug)
        used.add(slug)


def fill_genre_slugs(apps, schema_editor):
    Genre = apps.get_model('films', 'Genre')
    used = set()
    for g in Genre.objects.order_by('id'):
        base = (slugify(g.genre, allow_unicode=True) or f'genre-{g.pk}')[:100]
        slug = base
        n = 1
        while slug in used:
            slug = f'{base}-{n}'
            n += 1
        Genre.objects.filter(pk=g.pk).update(slug=slug)
        used.add(slug)


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0007_promobanner'),
    ]

    operations = [
        # 1. Сначала расширяем колонки — AlterField ДО RunPython
        migrations.AlterField(
            model_name='film',
            name='slug',
            field=models.SlugField(
                allow_unicode=True,
                blank=True,
                max_length=220,
                null=True,
                unique=True,
                verbose_name='Slug (URL)',
            ),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(
                allow_unicode=True,
                blank=True,
                max_length=120,
                null=True,
                unique=True,
            ),
        ),

        # 2. Теперь заполняем данные — колонка уже нужного размера
        migrations.RunPython(fill_film_slugs, migrations.RunPython.noop),
        migrations.RunPython(fill_genre_slugs, migrations.RunPython.noop),
    ]
