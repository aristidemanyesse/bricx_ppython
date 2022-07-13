# Generated by Django 4.0.4 on 2022-07-13 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisationApp', '0001_initial'),
        ('approvisionnementApp', '0001_initial'),
        ('coreApp', '0001_initial'),
        ('productionApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ligneapprovisionnement',
            name='ressource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ressource_ligneapprovisionnement', to='productionApp.ressource'),
        ),
        migrations.AddField(
            model_name='ligneachatstock',
            name='achatstock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achatstock_ligne', to='approvisionnementApp.achatstock'),
        ),
        migrations.AddField(
            model_name='ligneachatstock',
            name='brique',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brique_ligneachatstock', to='productionApp.brique'),
        ),
        migrations.AddField(
            model_name='fournisseur',
            name='agence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_fournisseur', to='organisationApp.agence'),
        ),
        migrations.AddField(
            model_name='approvisionnement',
            name='agence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_approvisionnement', to='organisationApp.agence'),
        ),
        migrations.AddField(
            model_name='approvisionnement',
            name='employe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employe_approvisionnement', to='organisationApp.employe'),
        ),
        migrations.AddField(
            model_name='approvisionnement',
            name='employe_reception',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employe_reception_approvisionnement', to='organisationApp.employe'),
        ),
        migrations.AddField(
            model_name='approvisionnement',
            name='etat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreApp.etat'),
        ),
        migrations.AddField(
            model_name='approvisionnement',
            name='fournisseur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fournisseur_approvisionnement', to='approvisionnementApp.fournisseur'),
        ),
        migrations.AddField(
            model_name='achatstock',
            name='agence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_achatstock', to='organisationApp.agence'),
        ),
        migrations.AddField(
            model_name='achatstock',
            name='employe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employe_achatstock', to='organisationApp.employe'),
        ),
        migrations.AddField(
            model_name='achatstock',
            name='employe_reception',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employe_reception_achatstock', to='organisationApp.employe'),
        ),
        migrations.AddField(
            model_name='achatstock',
            name='etat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreApp.etat'),
        ),
        migrations.AddField(
            model_name='achatstock',
            name='fournisseur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fournisseur_achatstock', to='approvisionnementApp.fournisseur'),
        ),
    ]
