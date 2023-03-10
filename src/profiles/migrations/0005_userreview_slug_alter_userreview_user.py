# Generated by Django 4.1.7 on 2023-02-19 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("profiles", "0004_userreview_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="userreview",
            name="slug",
            field=models.SlugField(default="", unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="userreview",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
