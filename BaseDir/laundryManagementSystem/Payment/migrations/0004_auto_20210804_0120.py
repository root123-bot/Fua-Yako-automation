# Generated by Django 3.0 on 2021-08-04 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payment', '0003_auto_20210804_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='account_number',
            field=models.CharField(default='no account added', max_length=25),
        ),
    ]