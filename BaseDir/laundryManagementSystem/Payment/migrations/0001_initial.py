# Generated by Django 3.0 on 2021-07-19 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=30)),
                ('account_number', models.PositiveIntegerField()),
                ('balance', models.PositiveIntegerField()),
            ],
        ),
    ]
