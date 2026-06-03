from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0004_remove_genre_choices_cartoon_proxy'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='age_rating',
            field=models.CharField(
                choices=[('0+', '0+'), ('6+', '6+'), ('12+', '12+'), ('16+', '16+'), ('18+', '18+')],
                default='0+',
                max_length=5,
                verbose_name='Возрастной рейтинг',
            ),
        ),
        migrations.AddField(
            model_name='showtime',
            name='rows',
            field=models.PositiveSmallIntegerField(default=10, verbose_name='Рядов в зале'),
        ),
        migrations.AddField(
            model_name='showtime',
            name='seats_per_row',
            field=models.PositiveSmallIntegerField(default=12, verbose_name='Мест в ряду'),
        ),
        migrations.AlterField(
            model_name='showtime',
            name='film',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name='showtimes',
                to='films.film',
                verbose_name='Фильм',
            ),
        ),
    ]
