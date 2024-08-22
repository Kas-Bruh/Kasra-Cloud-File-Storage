# Generated by Django 5.0.7 on 2024-08-11 05:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_folder_file_navigator_delete_navigatormodel"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="folder",
            name="owner",
        ),
        migrations.RemoveField(
            model_name="folder",
            name="parent_folder",
        ),
        migrations.RemoveField(
            model_name="navigator",
            name="root_folder",
        ),
        migrations.RemoveField(
            model_name="navigator",
            name="user",
        ),
        migrations.CreateModel(
            name="NavigatorModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.TextField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="File",
        ),
        migrations.DeleteModel(
            name="Folder",
        ),
        migrations.DeleteModel(
            name="Navigator",
        ),
    ]
