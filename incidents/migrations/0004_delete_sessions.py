# Generated by Django 4.0.2 on 2022-03-23 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0003_sessions_logs_event_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Sessions',
        ),
    ]
