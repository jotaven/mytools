# Generated by Django 5.0.6 on 2024-05-23 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytools', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='context',
            name='slug',
            field=models.SlugField(blank=True, max_length=6, unique=True),
        ),
    ]
