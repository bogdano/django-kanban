# Generated by Django 4.2.7 on 2023-11-28 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('items', '0005_alter_item_author_alter_item_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
