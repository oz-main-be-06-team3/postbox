# Generated by Django 5.1.3 on 2024-12-02 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_users_email_verification_token"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="users",
            name="username",
        ),
    ]