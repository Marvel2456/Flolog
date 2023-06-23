# Generated by Django 4.2 on 2023-06-22 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biodata', '0004_rename_allergy_name_allergy_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalrecord',
            name='age',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='medicalrecord',
            name='blood_group',
            field=models.CharField(blank=True, choices=[('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')], default='O+', max_length=10, null=True),
        ),
    ]