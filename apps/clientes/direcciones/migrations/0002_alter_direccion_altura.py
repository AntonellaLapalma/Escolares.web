# Generated by Django 4.1.7 on 2023-11-03 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('direcciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccion',
            name='altura',
            field=models.CharField(max_length=20),
        ),
    ]
