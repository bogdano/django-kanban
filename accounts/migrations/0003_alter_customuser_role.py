# Generated by Django 4.2.7 on 2023-11-16 18:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_rename_age_customuser_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="role",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
