# Generated by Django 3.1.7 on 2021-06-09 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowlingapp', '0018_auto_20210609_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='money',
            name='max',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='money',
            name='min',
            field=models.IntegerField(default=0),
        ),
    ]
