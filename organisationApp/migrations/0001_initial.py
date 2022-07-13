# Generated by Django 4.0.4 on 2022-07-13 13:51

from django.conf import settings
import django.contrib.auth.models
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
            name='Agence',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('lieu', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('telephone', models.CharField(blank=True, max_length=255, null=True)),
                ('adresse', models.CharField(blank=True, max_length=255, null=True)),
                ('contact', models.CharField(blank=True, max_length=255, null=True)),
                ('is_never_connected', models.BooleanField(default=True)),
                ('is_allowed', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, default='default.png', max_length=255, null=True, upload_to='stockage/images/employes/')),
                ('brut', models.CharField(blank=True, max_length=255, null=True)),
                ('agence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_employe', to='organisationApp.agence')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user', models.Model),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
