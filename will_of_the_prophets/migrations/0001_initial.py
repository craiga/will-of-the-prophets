# Generated by Django 2.0.5 on 2018-05-27 11:29  # noqa: D100

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import will_of_the_prophets.models
import will_of_the_prophets.validators


class Migration(migrations.Migration):  # noqa: D101
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Butthole",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "start_square",
                    models.PositiveIntegerField(
                        unique=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(100),
                            will_of_the_prophets.validators.not_special_square_validator,
                        ],
                    ),
                ),
                (
                    "end_square",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(100),
                        ]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Roll",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "number",
                    models.PositiveIntegerField(
                        default=will_of_the_prophets.models.default_roll_number
                    ),
                ),
                ("embargo", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="SpecialSquare",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "square",
                    models.PositiveIntegerField(
                        unique=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(100),
                            will_of_the_prophets.validators.not_butthole_start_validator,
                        ],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SpecialSquareType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("description", models.TextField()),
                ("image", models.ImageField(upload_to="special_square")),
            ],
        ),
        migrations.AddField(
            model_name="specialsquare",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="squares",
                to="will_of_the_prophets.SpecialSquareType",
            ),
        ),
    ]
