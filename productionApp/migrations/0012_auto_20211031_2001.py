# Generated by Django 3.2.8 on 2021-10-31 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productionApp', '0011_auto_20211031_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exigenceproduction',
            name='quantite',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='initialbriqueagence',
            name='quantite',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='ligneexigenceproduction',
            name='quantite',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
