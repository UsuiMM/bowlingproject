# Generated by Django 3.1.7 on 2021-06-10 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowlingapp', '0022_auto_20210610_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamemodel',
            name='ave',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gamemodel',
            name='max',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gamemodel',
            name='min',
            field=models.IntegerField(default=0),
        ),
    ]
