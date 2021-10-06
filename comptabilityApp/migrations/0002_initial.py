# Generated by Django 3.2.7 on 2021-10-05 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('approvisionnementApp', '0002_initial'),
        ('coreApp', '0001_initial'),
        ('livraisonApp', '0001_initial'),
        ('commandeApp', '0002_initial'),
        ('comptabilityApp', '0001_initial'),
        ('organisationApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfertfond',
            name='employe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employe_transfertfond', to='organisationApp.employe'),
        ),
        migrations.AddField(
            model_name='transfertfond',
            name='etat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coreApp.etat'),
        ),
        migrations.AddField(
            model_name='reglementtricycle',
            name='reglement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reglement_tricycle', to='comptabilityApp.reglement'),
        ),
        migrations.AddField(
            model_name='reglementtricycle',
            name='tricycle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tricycle_reglement', to='livraisonApp.tricycle'),
        ),
        migrations.AddField(
            model_name='reglementcommande',
            name='commande',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commande_reglement', to='commandeApp.commande'),
        ),
        migrations.AddField(
            model_name='reglementcommande',
            name='reglement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reglement_commande', to='comptabilityApp.reglement'),
        ),
        migrations.AddField(
            model_name='reglementapprovisionnement',
            name='approvisionnement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvisionnement_reglement', to='approvisionnementApp.approvisionnement'),
        ),
        migrations.AddField(
            model_name='reglementapprovisionnement',
            name='reglement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reglement_approvisionnement', to='comptabilityApp.reglement'),
        ),
        migrations.AddField(
            model_name='reglementachatstock',
            name='achatstock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achatstock_reglement', to='approvisionnementApp.achatstock'),
        ),
        migrations.AddField(
            model_name='reglementachatstock',
            name='reglement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reglement_achatstock', to='comptabilityApp.reglement'),
        ),
        migrations.AddField(
            model_name='reglement',
            name='etat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coreApp.etat'),
        ),
        migrations.AddField(
            model_name='reglement',
            name='mouvement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mouvement_reglement', to='comptabilityApp.mouvement'),
        ),
        migrations.AddField(
            model_name='reglement',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commande_reglement', to='comptabilityApp.typereglement'),
        ),
        migrations.AddField(
            model_name='operation',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_operation', to='comptabilityApp.categoryoperation'),
        ),
        migrations.AddField(
            model_name='operation',
            name='etat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coreApp.etat'),
        ),
        migrations.AddField(
            model_name='operation',
            name='mouvement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mouvement_operation', to='comptabilityApp.mouvement'),
        ),
        migrations.AddField(
            model_name='mouvement',
            name='compte',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='compte_mouvement', to='comptabilityApp.compte'),
        ),
        migrations.AddField(
            model_name='mouvement',
            name='employe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employe_payetricycle', to='organisationApp.employe'),
        ),
        migrations.AddField(
            model_name='mouvement',
            name='etat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coreApp.etat'),
        ),
        migrations.AddField(
            model_name='mouvement',
            name='mode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modepayement_mouvement', to='comptabilityApp.modepayement'),
        ),
        migrations.AddField(
            model_name='mouvement',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type_mouvement', to='comptabilityApp.typemouvement'),
        ),
        migrations.AddField(
            model_name='modepayement',
            name='etat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreApp.etat'),
        ),
        migrations.AddField(
            model_name='compte',
            name='agence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_compte', to='organisationApp.agence'),
        ),
        migrations.AddField(
            model_name='categoryoperation',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_categorie', to='comptabilityApp.typeoperationcaisse'),
        ),
    ]
