# Generated by Django 5.0.6 on 2024-05-28 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0002_alter_reservation_num_tickets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
