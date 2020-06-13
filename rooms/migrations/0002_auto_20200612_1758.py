# Generated by Django 3.0.7 on 2020-06-12 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('abstractitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rooms.AbstractItem')),
            ],
            options={
                'verbose_name_plural': 'Amenities',
            },
            bases=('rooms.abstractitem',),
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('abstractitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rooms.AbstractItem')),
            ],
            options={
                'verbose_name_plural': 'Facilities',
            },
            bases=('rooms.abstractitem',),
        ),
        migrations.CreateModel(
            name='HouseRule',
            fields=[
                ('abstractitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rooms.AbstractItem')),
            ],
            options={
                'verbose_name': 'House Rule',
            },
            bases=('rooms.abstractitem',),
        ),
        migrations.AlterModelOptions(
            name='roomtype',
            options={'verbose_name': 'Room Type'},
        ),
        migrations.RemoveField(
            model_name='room',
            name='room_type',
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rooms.RoomType'),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=80)),
                ('file', models.ImageField(upload_to='')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Room')),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='amenity',
            field=models.ManyToManyField(to='rooms.Amenity'),
        ),
        migrations.AddField(
            model_name='room',
            name='facility',
            field=models.ManyToManyField(to='rooms.Facility'),
        ),
        migrations.AddField(
            model_name='room',
            name='house_rule',
            field=models.ManyToManyField(to='rooms.HouseRule'),
        ),
    ]
