# Generated by Django 4.2 on 2023-06-29 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biodata', '0006_alter_medicalrecord_height_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='allergy',
            name='is_toggled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='history',
            name='is_toggled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='riskfactor',
            name='is_toggled',
            field=models.BooleanField(default=False),
        ),
    ]