from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0009_merge_20260602_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='is_slider',
            field=models.BooleanField(default=False, verbose_name='В карусель (герой-слайдер)'),
        ),
        migrations.AddField(
            model_name='film',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='В промо-баннер (главная)'),
        ),
    ]
