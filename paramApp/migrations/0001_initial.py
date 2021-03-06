# Generated by Django 4.0.4 on 2022-07-13 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyApp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('socialreason', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('contact', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('adresse', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('fax', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('postale', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('devise', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('image', models.ImageField(blank=True, max_length=255, null=True, upload_to='stockage/images/params/')),
                ('allow_waiting_payment', models.BooleanField(blank=True, default=True, null=True)),
                ('tva', models.IntegerField(blank=True, default=0, null=True)),
                ('seuil_credit', models.IntegerField(blank=True, default=0, null=True)),
                ('production_auto', models.BooleanField(blank=True, default=True, null=True)),
            ],
            options={
                'permissions': [('fabrique', '~ Acccès à la gestion de la fabrique'), ('boutique', '~ Acccès à la gestion de la boutique'), ('production', '~ Acccès à la gestion de la production'), ('organisation', "~ Acccès à la gestion de l'organisation"), ('commande', '~ Acccès à la gestion des commande'), ('livraison', '~ Acccès à la gestion des livraisons'), ('stock', '~ Acccès à la gestion des stock'), ('approvisionnement', '~ Acccès à la gestion des approvisionnements'), ('comptabilite', '~ Acccès à la gestion des comptabilité'), ('tresorerie', '~ Acccès à la tresorerie'), ('administration', '~ Acccès aux administrations'), ('manager', '~ Acccès à la gestion globale'), ('role', '~ Acccès aux accès utilisateurs'), ('CREATE', '~ Peut enregistrer des informations'), ('UPDATE', '~ Peut modifier des informations'), ('DELETE', '~ Peut supprimer des informations')],
            },
        ),
        migrations.CreateModel(
            name='MyCompte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifiant', models.CharField(max_length=255)),
                ('expiration', models.DateTimeField(default='')),
                ('tentative', models.IntegerField(default=3)),
            ],
        ),
    ]
