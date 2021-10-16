# Generated by Django 3.2.8 on 2021-10-15 00:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AchatStock',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('reference', models.CharField(max_length=255)),
                ('montant', models.IntegerField(default=0)),
                ('avance', models.IntegerField(default=0)),
                ('reste', models.IntegerField(default=0)),
                ('comment', models.TextField(default='')),
                ('datelivraison', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Approvisionnement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('reference', models.CharField(max_length=255)),
                ('montant', models.IntegerField(default=0)),
                ('avance', models.IntegerField(default=0)),
                ('reste', models.IntegerField(default=0)),
                ('transport', models.IntegerField(default=0)),
                ('comment', models.TextField(default='')),
                ('datelivraison', models.DateTimeField(blank=True, null=True)),
                ('acompteFournisseur', models.IntegerField(default=0)),
                ('detteFournisseur', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('fullname', models.CharField(max_length=255)),
                ('adresse', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('contact', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(default='')),
                ('acompte_initial', models.IntegerField(default=0)),
                ('dette_initial', models.IntegerField(default=0)),
                ('seuil_credit', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LigneAchatStock',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('quantite', models.IntegerField(default=0)),
                ('quantite_recu', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LigneApprovisionnement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('quantite', models.IntegerField(default=0)),
                ('quantite_recu', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('approvisionnement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvisionnement_ligne', to='approvisionnementApp.approvisionnement')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
