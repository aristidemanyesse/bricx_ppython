# Generated by Django 3.2.8 on 2021-10-25 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approvisionnementApp', '0003_auto_20211020_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achatstock',
            name='comment',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='approvisionnement',
            name='comment',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='fournisseur',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]