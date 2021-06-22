# Generated by Django 3.1.7 on 2021-06-09 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowlingapp', '0008_auto_20210605_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membername', models.CharField(max_length=100)),
                ('game_set_member', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Money',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_date', models.DateTimeField(verbose_name='日付')),
                ('detail', models.CharField(max_length=200)),
                ('cost', models.IntegerField(default=0)),
            ],
        ),
    ]
