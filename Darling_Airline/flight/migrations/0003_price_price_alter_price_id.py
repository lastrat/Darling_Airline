# Generated by Django 5.0.6 on 2024-05-31 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0002_price_flight_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='price',
            field=models.IntegerField(default=200),
        ),
        migrations.AlterField(
            model_name='price',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]