# Generated by Django 4.2.7 on 2023-12-04 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websightings_app', '0002_sighting'),
    ]

    operations = [
        migrations.AddField(
            model_name='sighting',
            name='skeptic',
            field=models.IntegerField(default=0),
        ),
    ]