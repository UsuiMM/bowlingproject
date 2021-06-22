# Generated by Django 3.1.7 on 2021-06-15 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowlingapp', '0027_money_pin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamemodel',
            name='point',
        ),
        migrations.AddField(
            model_name='gamemodel',
            name='point_total',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='teamcalculusmodel',
            name='point_alloc',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
