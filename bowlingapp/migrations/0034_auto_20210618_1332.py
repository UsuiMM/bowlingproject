# Generated by Django 3.1.7 on 2021-06-18 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowlingapp', '0033_auto_20210618_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='membermodel',
            name='ave',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='membermodel',
            name='max',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='membermodel',
            name='min',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='membermodel',
            name='point_total',
            field=models.IntegerField(default=0),
        ),
    ]