# Generated by Django 3.2.8 on 2021-10-25 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandeApp', '0006_conversion_ligneconversion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='comment',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
