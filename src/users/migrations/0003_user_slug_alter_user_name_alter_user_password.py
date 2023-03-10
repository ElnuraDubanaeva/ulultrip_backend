# Generated by Django 4.1.7 on 2023-02-18 09:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="slug",
            field=models.SlugField(
                default="", max_length=100, unique=True, verbose_name="URl"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=50),
        ),
    ]
