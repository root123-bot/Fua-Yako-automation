# Generated by Django 3.0 on 2021-07-21 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='account_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]