# Generated by Django 3.2.8 on 2021-10-22 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productionApp', '0004_auto_20211021_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='ressource',
            name='unite',
            field=models.CharField(default='', max_length=255),
        ),
    ]
