# Generated by Django 3.2.7 on 2021-09-22 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisationApp', '0001_initial'),
        ('commandeApp', '0001_initial'),
        ('coreApp', '__first__'),
    ]

    operations = [
        migrations.AddField(
            model_name='zonelivraison',
            name='agence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_zone', to='organisationApp.agence'),
        ),
        migrations.AddField(
            model_name='vehicule',
            name='etat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreApp.etat'),
        ),
        migrations.AddField(
            model_name='tricycle',
            name='etat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreApp.etat'),
        ),
        migrations.AddField(
            model_name='tricycle',
            name='livraison',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livraison_tricycle', to='commandeApp.livraison'),
        ),
    ]
