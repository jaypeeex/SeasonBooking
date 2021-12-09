# Generated by Django 3.1.1 on 2021-12-03 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('date', models.DateField()),
            ],
            options={
                'db_table': 'inventory',
            },
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('inventory', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='inventory.inventory')),
                ('item', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='items.item')),
            ],
            options={
                'db_table': 'inventory_item',
            },
        ),
    ]
