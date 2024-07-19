# Generated by Django 2.2 on 2024-07-18 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0003_auto_20240716_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='stock',
            field=models.IntegerField(default=0, help_text='Cantidad disponible en stock'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='descuento',
            field=models.IntegerField(default=0, help_text='Descuento'),
        ),
    ]