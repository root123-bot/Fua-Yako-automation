# Generated by Django 3.0 on 2021-07-15 15:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addtocart', '0039_auto_20210715_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='arrived_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 7, 15, 15, 24, 2, 608916), null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='finished_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 7, 17, 15, 24, 2, 607584), null=True),
        ),
    ]