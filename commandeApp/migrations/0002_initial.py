# Generated by Django 3.2.8 on 2021-11-01 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coreApp', '0001_initial'),
        ('organisationApp', '0001_initial'),
        ('commandeApp', '0001_initial'),
        ('clientApp', '0002_initial'),
        ('productionApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='zonelivraison',
            name='agence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_zone', to='organisationApp.agence'),
        ),
        migrations.AddField(
            model_name='prixzonelivraison',
            name='brique',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brique_zoneprix', to='productionApp.brique'),
        ),
        migrations.AddField(
            model_name='prixzonelivraison',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zone_prix', to='commandeApp.zonelivraison'),
        ),
        migrations.AddField(
            model_name='ligneconversion',
            name='brique',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brique_conversionligne', to='productionApp.brique'),
        ),
        migrations.AddField(
            model_name='ligneconversion',
            name='conversion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversion_ligne', to='commandeApp.conversion'),
        ),
        migrations.AddField(
            model_name='lignecommande',
            name='brique',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brique_lignecommande', to='productionApp.brique'),
        ),
        migrations.AddField(
            model_name='lignecommande',
            name='commande',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commande_ligne', to='commandeApp.commande'),
        ),
        migrations.AddField(
            model_name='groupecommande',
            name='agence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_groupecommande', to='organisationApp.agence'),
        ),
        migrations.AddField(
            model_name='groupecommande',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_groupecommande', to='clientApp.client'),
        ),
        migrations.AddField(
            model_name='groupecommande',
            name='etat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreApp.etat'),
        ),
        migrations.AddField(
            model_name='conversion',
            name='agence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_conversion', to='organisationApp.agence'),
        ),
        migrations.AddField(
            model_name='conversion',
            name='employe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employe_transfertstock', to='organisationApp.employe'),
        ),
        migrations.AddField(
            model_name='conversion',
            name='groupecommande_new',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_groupecommande_conversion', to='commandeApp.groupecommande'),
        ),
        migrations.AddField(
            model_name='conversion',
            name='groupecommande_old',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='old_groupecommande_conversion', to='commandeApp.groupecommande'),
        ),
        migrations.AddField(
            model_name='commande',
            name='agence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_commande', to='organisationApp.agence'),
        ),
        migrations.AddField(
            model_name='commande',
            name='employe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employe_commande', to='organisationApp.employe'),
        ),
        migrations.AddField(
            model_name='commande',
            name='groupecommande',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commande_groupecommande', to='commandeApp.groupecommande'),
        ),
        migrations.AddField(
            model_name='commande',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zone_commande', to='commandeApp.zonelivraison'),
        ),
    ]
