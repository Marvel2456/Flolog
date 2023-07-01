# Generated by Django 4.2 on 2023-07-01 06:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=250, null=True)),
                ('state', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.CharField(blank=True, max_length=250, null=True)),
                ('otp', models.CharField(blank=True, max_length=150, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_client', models.BooleanField(default=False)),
                ('is_pharmacist', models.BooleanField(default=False)),
                ('is_google_user', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('email', models.EmailField(max_length=250, unique=True)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='upload/client profile')),
                ('coin', models.PositiveIntegerField(blank=True, default=1)),
                ('country', models.CharField(blank=True, max_length=250, null=True)),
                ('state', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.CharField(blank=True, max_length=250, null=True)),
                ('referral_code', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pharmacist',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('balance', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='upload/pharma profile')),
                ('referral_code', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('paystack_charge_id', models.CharField(blank=True, default='', max_length=100)),
                ('paystack_access_code', models.CharField(blank=True, default='', max_length=100)),
                ('amount', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('paid', models.BooleanField(blank=True, default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.client')),
                ('plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.plan')),
            ],
            options={
                'verbose_name_plural': 'payment histories',
            },
        ),
        migrations.AddField(
            model_name='client',
            name='referred_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.pharmacist'),
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CareForm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('patient', models.CharField(blank=True, max_length=250, null=True)),
                ('drug_history', models.TextField(blank=True, null=True)),
                ('main_diagnosis', models.TextField(blank=True, null=True)),
                ('intervention_prescription', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('pharmacist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.pharmacist')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('action', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'activities',
                'ordering': ['-timestamp'],
            },
        ),
    ]
