# Generated by Django 5.0.4 on 2024-05-16 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
