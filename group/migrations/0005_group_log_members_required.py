# Generated by Django 3.2.5 on 2022-11-01 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0004_auto_20221101_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='group_log',
            name='members_required',
            field=models.IntegerField(default=2),
        ),
    ]