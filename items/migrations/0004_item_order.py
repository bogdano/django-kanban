# Generated by Django 4.2.7 on 2023-11-17 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_activity_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
