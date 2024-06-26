# Generated by Django 5.0.6 on 2024-05-31 20:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aeroplane',
            fields=[
                ('aero_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('aero_model', models.CharField(max_length=30)),
                ('tot_first_class', models.IntegerField()),
                ('tot_economy', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('f_id', models.AutoField(primary_key=True, serialize=False)),
                ('dest_airport', models.CharField(max_length=50)),
                ('depart_airport', models.CharField(max_length=50)),
                ('departure_time', models.DateTimeField()),
                ('duration', models.IntegerField()),
                ('available_place', models.IntegerField()),
                ('is_active', models.BooleanField()),
                ('aero_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.aeroplane')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('class_type', models.CharField(max_length=30)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('price', models.IntegerField(default=200)),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.flight')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservationId', models.AutoField(primary_key=True, serialize=False)),
                ('ticket_categories', models.CharField(max_length=25)),
                ('num_tickets', models.IntegerField()),
                ('total_price', models.FloatField()),
                ('is_paid', models.BooleanField(default=0)),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.flight')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.user')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(max_length=50)),
                ('reservation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.reservation')),
            ],
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('stop_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('airport_name', models.CharField(max_length=50)),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.flight')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('ticket_class', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('seat_number', models.IntegerField()),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.flight')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.user')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('num', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('mail', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('msg', models.CharField(max_length=150)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.user')),
            ],
        ),
    ]
