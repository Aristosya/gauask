# Generated by Django 4.0.2 on 2022-07-20 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_rename_creator_lecturer_lecturer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='lecturer',
        ),
    ]
