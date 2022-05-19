# Generated by Django 3.2.9 on 2021-11-15 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisationApp', '0001_initial'),
        ('authApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesagence',
            name='agence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agence_acces', to='organisationApp.agence'),
        ),
        migrations.AddField(
            model_name='accesagence',
            name='employe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employe_acces', to='organisationApp.employe'),
        ),
    ]
