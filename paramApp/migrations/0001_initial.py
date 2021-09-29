# Generated by Django 3.2.7 on 2021-09-29 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyCompte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifiant', models.CharField(max_length=255)),
                ('expired', models.DateTimeField(auto_now_add=True)),
                ('tentative', models.IntegerField(default=3)),
            ],
        ),
        migrations.CreateModel(
            name='Params',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('socialreason', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
                ('fax', models.CharField(max_length=255)),
                ('postale', models.CharField(max_length=255)),
                ('devise', models.CharField(max_length=255)),
                ('logo', models.ImageField(max_length=255, upload_to='')),
                ('allow_waiting_payment', models.BooleanField(default=True)),
                ('tva', models.BooleanField(default=True)),
                ('seuil_credit', models.BooleanField(default=True)),
                ('production_auto', models.BooleanField(default=True)),
                ('rupture_stock', models.BooleanField(default=True)),
            ],
        ),
    ]
