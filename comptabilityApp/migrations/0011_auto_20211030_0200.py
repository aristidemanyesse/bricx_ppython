# Generated by Django 3.2.8 on 2021-10-30 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptabilityApp', '0010_auto_20211029_2205'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TypeReglement',
        ),
        migrations.AlterField(
            model_name='categoryoperation',
            name='etiquette',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='modepayement',
            name='etiquette',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
