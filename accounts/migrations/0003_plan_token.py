# Generated by Django 4.2 on 2023-07-07 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_profile_pic_alter_client_profile_pic_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='token',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]