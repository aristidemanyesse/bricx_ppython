# Generated by Django 4.0.4 on 2022-07-13 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('approvisionnementApp', '0002_initial'),
        ('clientApp', '0002_initial'),
        ('commandeApp', '0002_initial'),
        ('comptabilityApp', '0001_initial'),
        ('organisationApp', '0001_initial'),
        ('livraisonApp', '0001_initial'),
        ('coreApp', '0001_initial'),
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
            name='mouvement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mouvement_reglement', to='comptabilityApp.mouvement'),
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
            name='mouvement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mouvement_reglement_commande', to='comptabilityApp.mouvement'),
        ),
        migrations.AddField(
            model_name='reglementapprovisionnement',
            name='approvisionnement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvisionnement_reglement', to='approvisionnementApp.approvisionnement'),
        ),
        migrations.AddField(
            model_name='reglementapprovisionnement',
            name='mouvement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mouvement_reglement_appro', to='comptabilityApp.mouvement'),
        ),
        migrations.AddField(
            model_name='reglementachatstock',
            name='achatstock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achatstock_reglement', to='approvisionnementApp.achatstock'),
        ),
        migrations.AddField(
            model_name='reglementachatstock',
            name='mouvement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mouvement_reglement_achatstock', to='comptabilityApp.mouvement'),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compte_mouvement', to='comptabilityApp.compte'),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_mouvement', to='comptabilityApp.typemouvement'),
        ),
        migrations.AddField(
            model_name='modepayement',
            name='etat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreApp.etat'),
        ),
        migrations.AddField(
            model_name='comptefournisseur',
            name='fournisseur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fournisseur_compte', to='approvisionnementApp.fournisseur'),
        ),
        migrations.AddField(
            model_name='comptefournisseur',
            name='mouvement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mouvement_comptefournisseur', to='comptabilityApp.mouvement'),
        ),
        migrations.AddField(
            model_name='compteclient',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_compte', to='clientApp.client'),
        ),
        migrations.AddField(
            model_name='compteclient',
            name='mouvement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mouvement_compteclient', to='comptabilityApp.mouvement'),
        ),
        migrations.AddField(
            model_name='compte',
            name='agence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agence_compte', to='organisationApp.agence'),
        ),
        migrations.AddField(
            model_name='categoryoperation',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_categorie', to='comptabilityApp.typeoperationcaisse'),
        ),
    ]
