# Generated by Django 3.2.8 on 2021-10-27 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('approvisionnementApp', '0006_remove_fournisseur_seuil_credit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fournisseur',
            old_name='logo',
            new_name='image',
        ),
    ]