# Generated by Django 5.1.5 on 2025-06-01 21:52

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="price_paid",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Suggested price in Nok",
                max_digits=5,
                validators=[django.core.validators.MinValueValidator(0.1)],
            ),
        ),
        migrations.CreateModel(
            name="DishRestaurantSuggestion",
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
                (
                    "dish_name",
                    models.CharField(help_text="Enter the dish name", max_length=45),
                ),
                (
                    "restaurant_name",
                    models.CharField(
                        help_text="Enter the restaurant name", max_length=45
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Suggested price in Nok",
                        max_digits=5,
                        validators=[django.core.validators.MinValueValidator(0.1)],
                    ),
                ),
                (
                    "available",
                    models.BooleanField(
                        default=True,
                        help_text="Check if this dish is currently available.",
                    ),
                ),
                ("description", models.TextField(blank=True)),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                (
                    "is_reviewed",
                    models.BooleanField(
                        default=False,
                        help_text="Set to True once an admin has processed this suggestion.",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Dish-Restaurant Suggestions",
                "ordering": ["-submitted_at"],
            },
        ),
    ]
