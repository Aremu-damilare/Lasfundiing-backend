# Generated by Django 4.1.4 on 2023-10-20 18:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0012_alter_kyc_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="kyc",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="kyc",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
