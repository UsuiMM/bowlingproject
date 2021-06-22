# Generated by Django 3.1.7 on 2021-06-09 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bowlingapp', '0012_money_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membermodel',
            name='game_set_member',
        ),
        migrations.AddField(
            model_name='membermodel',
            name='type_name',
            field=models.TextField(blank=True, verbose_name='メンバー名'),
        ),
        migrations.AddField(
            model_name='money',
            name='membername',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bowlingapp.membermodel'),
        ),
    ]