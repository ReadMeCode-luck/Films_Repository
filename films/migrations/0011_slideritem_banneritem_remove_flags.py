from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0010_film_is_slider_is_banner'),
    ]

    operations = [
        # Убираем флаги с Film
        migrations.RemoveField(model_name='film', name='is_slider'),
        migrations.RemoveField(model_name='film', name='is_banner'),

        # Создаём SliderItem
        migrations.CreateModel(
            name='SliderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(
                    choices=[(i, str(i)) for i in range(1, 11)],
                    unique=True,
                    verbose_name='Позиция (1–10)'
                )),
                ('film', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='films.film',
                    verbose_name='Фильм'
                )),
            ],
            options={
                'verbose_name': 'Слайд',
                'verbose_name_plural': 'Слайдер (главная)',
                'ordering': ['order'],
            },
        ),

        # Создаём BannerItem
        migrations.CreateModel(
            name='BannerItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('film', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='films.film',
                    verbose_name='Фильм'
                )),
            ],
            options={
                'verbose_name': 'Промо-баннер',
                'verbose_name_plural': 'Промо-баннер (главная)',
            },
        ),
    ]
