from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0013_favorite'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='tickets',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Покупатель'
            ),
        ),
        migrations.AddField(
            model_name='ticket',
            name='bought_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата покупки'),
        ),
    ]
