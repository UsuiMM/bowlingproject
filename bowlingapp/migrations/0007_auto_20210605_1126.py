# Generated by Django 3.1.7 on 2021-06-05 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowlingapp', '0006_auto_20210605_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membermodel',
            name='game_set_member',
            field=models.TextField(max_length=100),
        ),
    ]
