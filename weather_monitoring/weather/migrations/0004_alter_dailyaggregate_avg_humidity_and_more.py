# Generated by Django 4.2.16 on 2024-10-24 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("weather", "0003_dailyaggregate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailyaggregate",
            name="avg_humidity",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="dailyaggregate",
            name="avg_temp",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="dailyaggregate",
            name="max_temp",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="dailyaggregate",
            name="max_wind_speed",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="dailyaggregate",
            name="min_temp",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
