# Generated by Django 4.1.7 on 2023-10-13 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empleados', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patente', models.CharField(max_length=20)),
                ('cant_asientos', models.CharField(max_length=50)),
                ('celador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='celador_de_vehiculo', to='empleados.empleado')),
                ('chofer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chofer_de_vehiculo', to='empleados.empleado')),
            ],
        ),
    ]
