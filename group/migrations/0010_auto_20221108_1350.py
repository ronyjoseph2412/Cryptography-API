# Generated by Django 3.2.5 on 2022-11-08 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0009_group_log_iv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group_log',
            name='iv',
        ),
        migrations.RemoveField(
            model_name='group_log',
            name='key',
        ),
    ]
