# Generated by Django 4.1.7 on 2023-03-17 10:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0014_alter_user_is_active_alter_user_username"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="name",
        ),
    ]
