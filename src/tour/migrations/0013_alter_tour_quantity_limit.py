# Generated by Django 4.1.7 on 2023-03-17 14:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tour", "0012_tour_qr_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tour",
            name="quantity_limit",
            field=models.PositiveIntegerField(),
        ),
    ]
