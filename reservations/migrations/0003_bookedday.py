# Generated by Django 3.0.8 on 2020-07-17 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200612_1629'),
        ('reservations', '0002_auto_20200613_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookedDay',
            fields=[
                ('timestampedmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.TimeStampedModel')),
                ('day', models.DateField()),
                ('reserve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.Reservation')),
            ],
            bases=('core.timestampedmodel',),
        ),
    ]
