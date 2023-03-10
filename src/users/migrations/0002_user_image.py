# Generated by Django 4.1.7 on 2023-02-18 08:51

from django.db import migrations, models
import src.users.utils


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="image",
            field=models.ImageField(
                blank=True,
                default="media/default_images/default_user_image.jpeg",
                null=True,
            ),
        ),
    ]
