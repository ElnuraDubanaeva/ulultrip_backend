# Generated by Django 4.1.7 on 2023-03-17 14:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tour", "0010_alter_tour_qr_code"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tour",
            name="qr_code",
        ),
    ]