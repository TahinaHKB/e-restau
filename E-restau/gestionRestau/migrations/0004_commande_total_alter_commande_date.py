# Generated by Django 5.0.4 on 2024-10-20 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionRestau', '0003_commande'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='total',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='commande',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]