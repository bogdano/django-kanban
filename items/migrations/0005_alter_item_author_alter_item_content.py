# Generated by Django 4.2.7 on 2023-11-17 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('items', '0004_item_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='content',
            field=models.CharField(max_length=500),
        ),
    ]
