# Generated by Django 5.1.3 on 2024-12-04 09:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Analysis",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("about", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=30)),
                ("period_start", models.DateTimeField()),
                ("period_end", models.DateTimeField()),
                ("result_image", models.ImageField(blank=True, null=True, upload_to="analysis/%Y/%m/%d/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "db_table": "analysis",
            },
        ),
    ]
