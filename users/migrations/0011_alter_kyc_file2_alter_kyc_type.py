# Generated by Django 4.1.4 on 2023-10-20 18:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0010_alter_withdrawal_amount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="kyc",
            name="file2",
            field=models.FileField(blank=True, null=True, upload_to="kyc_files/"),
        ),
        migrations.AlterField(
            model_name="kyc",
            name="type",
            field=models.CharField(
                choices=[
                    ("drivers_license", "Driver's License"),
                    ("voters_card", "Voter's Card"),
                    ("NIN", "National Identification Number (NIN)"),
                    ("international_passport", "International Passport"),
                ],
                max_length=150,
            ),
        ),
    ]