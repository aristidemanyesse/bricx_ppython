# Generated by Django 3.2.7 on 2021-10-05 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisationApp', '0001_initial'),
        ('clientApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='agence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_agence', to='organisationApp.agence'),
        ),
        migrations.AddField(
            model_name='client',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_client', to='clientApp.typeclient'),
        ),
    ]