# Generated by Django 4.0.2 on 2022-03-23 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0004_delete_sessions'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='page',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
