# Generated by Django 5.0.1 on 2024-02-02 17:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantapp', '0003_alter_orderplaced_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='customer',
            field=models.ForeignKey(db_column='cust_id', on_delete=django.db.models.deletion.CASCADE, to='restaurantapp.customer'),
        ),
    ]