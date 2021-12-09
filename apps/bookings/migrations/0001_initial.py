# Generated by Django 3.1.1 on 2021-12-03 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('extra_services', '0001_initial'),
        ('apartments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.CharField(max_length=15, unique=True)),
                ('created_at', models.DateTimeField()),
                ('modified_at', models.DateTimeField()),
                ('is_canceled', models.BooleanField(default=False)),
                ('canceled_at', models.DateTimeField(default=None, null=True)),
                ('total_amount', models.IntegerField()),
                ('is_paid', models.BooleanField(default=False)),
                ('stay_from', models.DateField()),
                ('stay_to', models.DateField()),
                ('guests_number', models.IntegerField()),
                ('apartment', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='apartments.apartment')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'booking',
            },
        ),
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.CharField(max_length=15)),
                ('arrival_date', models.DateField()),
                ('departure_date', models.DateField()),
                ('arrival_time', models.TimeField()),
                ('departure_time', models.TimeField()),
                ('guests_number', models.IntegerField()),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('check_in_staff', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'check_in',
            },
        ),
        migrations.CreateModel(
            name='BookingExtraService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_booking_total_amount', models.IntegerField()),
                ('booking', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='bookings.booking')),
                ('extra_service', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='extra_services.extraservice')),
            ],
            options={
                'db_table': 'booking_extra_service',
            },
        ),
    ]