# Generated by Django 3.2.9 on 2021-11-09 09:19

import django.contrib.admin.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('etiquette', models.CharField(max_length=255)),
                ('classe', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('logentry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='admin.logentry')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            bases=('admin.logentry', models.Model),
            managers=[
                ('objects', django.contrib.admin.models.LogEntryManager()),
            ],
        ),
    ]
