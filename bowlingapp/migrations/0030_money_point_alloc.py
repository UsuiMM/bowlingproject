# Generated by Django 3.1.7 on 2021-06-15 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowlingapp', '0029_auto_20210615_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='money',
            name='point_alloc',
            field=models.IntegerField(default=0),
        ),
    ]
