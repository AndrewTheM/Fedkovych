# Generated by Django 5.1 on 2024-08-22 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Song",
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
                ("title", models.CharField(max_length=255)),
                ("mp3_file", models.FileField(upload_to="static/audio/")),
                ("date_added", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Пісня",
                "verbose_name_plural": "Пісні",
                "ordering": ["-date_added"],
            },
        ),
        migrations.CreateModel(
            name="Video",
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
                ("title", models.CharField(max_length=255)),
                ("mp4_file", models.FileField(upload_to="static/video/")),
                ("date_added", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Відео",
                "verbose_name_plural": "Відео",
                "ordering": ["-date_added"],
            },
        ),
    ]
