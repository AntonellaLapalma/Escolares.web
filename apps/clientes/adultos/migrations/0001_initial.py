# Generated by Django 4.1.7 on 2023-10-13 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('familias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parentesco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parentesco', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Adulto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('celular', models.CharField(max_length=20)),
                ('id_familiar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='familias.familia')),
                ('parentesco', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='adultos.parentesco')),
            ],
        ),
    ]
