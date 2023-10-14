# Generated by Django 4.1.4 on 2023-10-14 14:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0004_order_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="profit",
            field=models.DecimalField(
                decimal_places=2, default=0.0, max_digits=6, null=True
            ),
        ),
    ]
