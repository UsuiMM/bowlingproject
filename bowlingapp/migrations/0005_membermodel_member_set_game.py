# Generated by Django 3.1.7 on 2021-06-05 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowlingapp', '0004_auto_20210604_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='membermodel',
            name='member_set_game',
            field=models.TextField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
