# Generated by Django 3.0 on 2021-07-07 16:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addtocart', '0018_auto_20210707_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='arrived_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 7, 7, 16, 27, 15, 338703), null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='finished_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 7, 9, 16, 27, 15, 336984), null=True),
        ),
    ]