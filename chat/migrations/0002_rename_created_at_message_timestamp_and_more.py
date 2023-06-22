# Generated by Django 4.2 on 2023-06-22 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='created_at',
            new_name='timestamp',
        ),
        migrations.RemoveField(
            model_name='message',
            name='chatroom',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender_role',
        ),
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='chat.chatroom'),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.client'),
        ),
    ]
