from django.db import migrations
import autoslug.fields
from django.utils.text import slugify


def fill_null_slugs(apps, schema_editor):
    """Заполняем slug у фильмов с NULL-значением."""
    Film = apps.get_model('films', 'Film')
    used = set(Film.objects.exclude(slug__isnull=True).exclude(slug='').values_list('slug', flat=True))
    for film in Film.objects.filter(slug__isnull=True).order_by('id'):
        base = slugify(film.title, allow_unicode=True) or f'film-{film.pk}'
        slug = base
        counter = 1
        while slug in used:
            slug = f'{base}-{counter}'
            counter += 1
        # Raw update — обходим любую логику AutoSlugField
        Film.objects.filter(pk=film.pk).update(slug=slug)
        used.add(slug)


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0005_film_age_rating_showtime_rows_seats'),
    ]

    # Только заполняем данные — схему не меняем (null=True остаётся)
    operations = [
        migrations.RunPython(fill_null_slugs, migrations.RunPython.noop),
    ]
