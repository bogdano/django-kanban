# Generated by Django 4.2.7 on 2023-12-02 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_alter_item_updated_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='display_date',
            field=models.DateField(null=True),
        ),
    ]
