# Generated by Django 2.0.5 on 2018-06-07 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0004_gallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='pic',
            field=models.ImageField(upload_to='pictures/Gallery/'),
        ),
    ]
