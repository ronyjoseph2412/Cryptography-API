# Generated by Django 3.2.5 on 2022-11-01 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_data',
            name='user_company',
        ),
    ]
