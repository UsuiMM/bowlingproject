# Generated by Django 3.1.7 on 2021-06-04 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowlingapp', '0003_auto_20210604_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membername', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='SampleModel',
        ),
    ]
