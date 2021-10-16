# Generated by Django 3.2.8 on 2021-10-16 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientApp', '0003_typeclient_etiquette'),
        ('comptabilityApp', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='compteclient',
            name='is_dette',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='compteclient',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_compte', to='clientApp.client'),
        ),
    ]