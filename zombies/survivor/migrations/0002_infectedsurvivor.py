# Generated by Django 3.1.1 on 2020-12-23 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survivor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfectedSurvivor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_by', to='survivor.survivor')),
                ('survivor_infected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survivor_infected', to='survivor.survivor')),
            ],
            options={
                'unique_together': {('reported_by', 'survivor_infected')},
            },
        ),
    ]
