# Generated by Django 3.2.8 on 2021-11-01 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productionApp', '0001_initial'),
        ('commandeApp', '0002_initial'),
        ('livraisonApp', '0001_initial'),
        ('coreApp', '0001_initial'),
        ('organisationApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicule',
            name='agence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_vehicule', to='organisationApp.agence'),
        ),
        migrations.AddField(
            model_name='tricycle',
            name='livraison',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livraison_tricycle', to='livraisonApp.livraison'),
        ),
        migrations.AddField(
            model_name='livraison',
            name='agence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_livraison', to='organisationApp.agence'),
        ),
        migrations.AddField(
            model_name='livraison',
            name='chauffeur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chauffeur_livraison', to='livraisonApp.chauffeur'),
        ),
        migrations.AddField(
            model_name='livraison',
            name='employe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employe_livraison', to='organisationApp.employe'),
        ),
        migrations.AddField(
            model_name='livraison',
            name='etat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreApp.etat'),
        ),
        migrations.AddField(
            model_name='livraison',
            name='groupecommande',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupecommande_livraison', to='commandeApp.groupecommande'),
        ),
        migrations.AddField(
            model_name='livraison',
            name='modelivraison',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mode_livraison', to='livraisonApp.modelivraison'),
        ),
        migrations.AddField(
            model_name='livraison',
            name='vehicule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicule_livraison', to='livraisonApp.vehicule'),
        ),
        migrations.AddField(
            model_name='livraison',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zone_livraison', to='commandeApp.zonelivraison'),
        ),
        migrations.AddField(
            model_name='lignelivraison',
            name='brique',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brique_lignelivraison', to='productionApp.brique'),
        ),
        migrations.AddField(
            model_name='lignelivraison',
            name='livraison',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livraison_ligne', to='livraisonApp.livraison'),
        ),
        migrations.AddField(
            model_name='chauffeur',
            name='agence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_chauffeur', to='organisationApp.agence'),
        ),
    ]
