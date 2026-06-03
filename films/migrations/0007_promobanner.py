from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0006_fix_film_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge_text', models.CharField(default='Премьера недели', max_length=60, verbose_name='Текст значка')),
                ('image', models.ImageField(upload_to='promo/', verbose_name='Фоновое изображение')),
                ('title', models.CharField(max_length=200, verbose_name='Название (крупно)')),
                ('subtitle', models.CharField(blank=True, max_length=200, verbose_name='Подзаголовок (розовый)')),
                ('description', models.TextField(blank=True, verbose_name='Описание / синопсис')),
                ('genre', models.CharField(blank=True, max_length=150, verbose_name='Жанр')),
                ('rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=3, verbose_name='IMDb рейтинг')),
                ('duration', models.PositiveIntegerField(default=0, verbose_name='Длительность (мин)')),
                ('button_url', models.CharField(blank=True, default='#', max_length=300, verbose_name='Ссылка кнопки «Смотреть»')),
                ('is_active', models.BooleanField(default=True, verbose_name='Показывать на сайте')),
            ],
            options={
                'verbose_name': 'Промо-баннер',
                'verbose_name_plural': 'Промо-баннер (главная)',
            },
        ),
    ]
