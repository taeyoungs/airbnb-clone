# Generated by Django 3.0.7 on 2020-06-16 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_auto_20200613_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to='rooms_photo'),
        ),
    ]
