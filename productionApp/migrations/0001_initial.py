# Generated by Django 3.2.9 on 2021-11-15 18:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisationApp', '0001_initial'),
        ('coreApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brique',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('comment', models.TextField(blank=True, default='', null=True)),
                ('alert_stock', models.IntegerField(blank=True, default=10, null=True)),
                ('image', models.ImageField(blank=True, default='', max_length=255, null=True, upload_to='stockage/images/briques/')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExigenceProduction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('quantite', models.IntegerField(blank=True, default=0, null=True)),
                ('brique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brique_exigenceproduction', to='productionApp.brique')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ressource',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('unite', models.CharField(default='', max_length=255)),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
                ('active', models.BooleanField(default=True)),
                ('alert_stock', models.IntegerField(blank=True, default=10, null=True)),
                ('comment', models.TextField(blank=True, default='', null=True)),
                ('image', models.ImageField(blank=True, default='', max_length=255, null=True, upload_to='stockage/images/ressources/')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TypePerte',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('etiquette', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('reference', models.CharField(max_length=255)),
                ('date', models.DateField(blank=True, null=True)),
                ('date_rangement', models.DateTimeField(blank=True, null=True)),
                ('montant_production', models.IntegerField(default=0)),
                ('montant_rangement', models.IntegerField(default=0)),
                ('montant_livraison', models.IntegerField(default=0)),
                ('comment', models.TextField(blank=True, default='', null=True)),
                ('agence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_production', to='organisationApp.agence')),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employe_production', to='organisationApp.employe')),
                ('employe_rangement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employe_rangement_production', to='organisationApp.employe')),
                ('etat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreApp.etat')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PerteRessource',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('quantite', models.FloatField(default=0)),
                ('comment', models.TextField(blank=True, default='', null=True)),
                ('agence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_perteressource', to='organisationApp.agence')),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employe_perteressource', to='organisationApp.employe')),
                ('ressource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ressource_perte', to='productionApp.ressource')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_perteressource', to='productionApp.typeperte')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PerteBrique',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('quantite', models.IntegerField(default=0)),
                ('comment', models.TextField(blank=True, default='', null=True)),
                ('agence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_perte', to='organisationApp.agence')),
                ('brique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brique_perte', to='productionApp.brique')),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employe_pertebrique', to='organisationApp.employe')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_pertebrique', to='productionApp.typeperte')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PayeBriqueFerie',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=0)),
                ('price_rangement', models.IntegerField(default=0)),
                ('price_livraison', models.IntegerField(default=0)),
                ('agence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_payeferie', to='organisationApp.agence')),
                ('brique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brique_payeferie', to='productionApp.brique')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PayeBrique',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=0)),
                ('price_rangement', models.IntegerField(default=0)),
                ('price_livraison', models.IntegerField(default=0)),
                ('agence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_paye', to='organisationApp.agence')),
                ('brique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brique_paye', to='productionApp.brique')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LigneProduction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('perte', models.IntegerField(default=0)),
                ('quantite', models.IntegerField(default=0)),
                ('brique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brique_ligneproduction', to='productionApp.brique')),
                ('production', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='production_ligne', to='productionApp.production')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LigneExigenceProduction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('quantite', models.FloatField(blank=True, default=0, null=True)),
                ('exigence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exigence_ligne', to='productionApp.exigenceproduction')),
                ('ressource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ressource_exigenceligne', to='productionApp.ressource')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LigneConsommation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('quantite', models.FloatField(default=0)),
                ('production', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='production_ligneconsommation', to='productionApp.production')),
                ('ressource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ressource_ligneconsommation', to='productionApp.ressource')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InitialRessourceAgence',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('quantite', models.FloatField(default=0)),
                ('agence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_initialressource', to='organisationApp.agence')),
                ('ressource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ressource_initialagence', to='productionApp.ressource')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InitialBriqueAgence',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('quantite', models.IntegerField(blank=True, default=0, null=True)),
                ('agence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_initialbrique', to='organisationApp.agence')),
                ('brique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brique_initialagence', to='productionApp.brique')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ConsommationJour',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('date', models.DateField(blank=True, default='', null=True)),
                ('comment', models.TextField(blank=True, default='', null=True)),
                ('employe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employe_consommationjour', to='organisationApp.employe')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
