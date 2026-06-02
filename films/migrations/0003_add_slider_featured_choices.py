from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_alter_film_options_film_country_film_duration_and_more'),
    ]

    operations = [
        # 1. Добавляем is_cartoon в Film
        migrations.AddField(
            model_name='film',
            name='is_cartoon',
            field=models.BooleanField(default=False, verbose_name='Мультфильм'),
        ),

        # 2. Меняем genre на choices
        migrations.AlterField(
            model_name='film',
            name='genre',
            field=models.CharField(
                blank=True,
                choices=[
                    ('Комедия', 'Комедия'),
                    ('Драма', 'Драма'),
                    ('Боевик', 'Боевик'),
                    ('Хоррор', 'Хоррор'),
                    ('Научная фантастика', 'Научная фантастика'),
                    ('Фэнтези', 'Фэнтези'),
                    ('Вестерн', 'Вестерн'),
                    ('Детектив', 'Детектив'),
                    ('Мюзикл', 'Мюзикл'),
                    ('Фильм-катастрофа', 'Фильм-катастрофа'),
                    ('Документальный', 'Документальный'),
                ],
                default='',
                max_length=50,
                verbose_name='Жанр',
            ),
        ),

        # 3. Меняем country на choices
        migrations.AlterField(
            model_name='film',
            name='country',
            field=models.CharField(
                blank=True,
                choices=[
                    ('Германия', 'Германия'),
                    ('Китай', 'Китай'),
                    ('Италия', 'Италия'),
                    ('Великобритания', 'Великобритания'),
                    ('Индия', 'Индия'),
                    ('Испания', 'Испания'),
                    ('Япония', 'Япония'),
                    ('Франция', 'Франция'),
                    ('Турция', 'Турция'),
                    ('Греция', 'Греция'),
                    ('Россия', 'Россия'),
                    ('США', 'США'),
                    ('Канада', 'Канада'),
                    ('Казахстан', 'Казахстан'),
                    ('Южная Корея', 'Южная Корея'),
                    ('Нигерия', 'Нигерия'),
                ],
                default='',
                max_length=100,
                verbose_name='Страна',
            ),
        ),

        # 4. Добавляем валидаторы года
        migrations.AlterField(
            model_name='film',
            name='year',
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1895),
                    django.core.validators.MaxValueValidator(2026),
                ],
                verbose_name='Год',
            ),
        ),

        # 5. Создаём модель Slider
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='slider/', verbose_name='Изображение')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('genre', models.CharField(blank=True, max_length=100, verbose_name='Жанр')),
                ('duration', models.PositiveIntegerField(default=0, verbose_name='Длительность (мин)')),
                ('rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=3, verbose_name='Рейтинг')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Слайд',
                'verbose_name_plural': 'Слайдер (главная)',
                'ordering': ['order'],
            },
        ),

        # 6. Создаём модель FeaturedFilm
        migrations.CreateModel(
            name='FeaturedFilm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField(
                    choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
                    unique=True,
                    verbose_name='Позиция (1–5)',
                )),
                ('film', models.OneToOneField(
                    limit_choices_to={'is_cartoon': False},
                    on_delete=django.db.models.deletion.CASCADE,
                    to='films.film',
                    verbose_name='Фильм',
                )),
            ],
            options={
                'verbose_name': 'Рекомендуемый фильм',
                'verbose_name_plural': 'Рекомендуемые фильмы (главная)',
                'ordering': ['position'],
            },
        ),

        # 7. Создаём модель FeaturedCartoon
        migrations.CreateModel(
            name='FeaturedCartoon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField(
                    choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
                    unique=True,
                    verbose_name='Позиция (1–5)',
                )),
                ('film', models.OneToOneField(
                    limit_choices_to={'is_cartoon': True},
                    on_delete=django.db.models.deletion.CASCADE,
                    to='films.film',
                    verbose_name='Мультфильм',
                )),
            ],
            options={
                'verbose_name': 'Рекомендуемый мультфильм',
                'verbose_name_plural': 'Рекомендуемые мультфильмы (главная)',
                'ordering': ['position'],
            },
        ),
    ]
