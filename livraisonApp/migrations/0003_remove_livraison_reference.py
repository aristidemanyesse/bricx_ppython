# Generated by Django 3.2.9 on 2021-12-07 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livraisonApp', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livraison',
            name='reference',
        ),
    ]