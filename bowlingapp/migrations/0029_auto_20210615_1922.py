# Generated by Django 3.1.7 on 2021-06-15 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowlingapp', '0028_auto_20210615_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamemodel',
            name='point_total',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='teamcalculusmodel',
            name='point_alloc',
            field=models.IntegerField(default=0),
        ),
    ]
