# Generated by Django 3.1.7 on 2021-06-17 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowlingapp', '0030_money_point_alloc'),
    ]

    operations = [
        migrations.AddField(
            model_name='money',
            name='point',
            field=models.IntegerField(default=0),
        ),
    ]
