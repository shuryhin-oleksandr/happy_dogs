# Generated by Django 3.1.13 on 2021-10-04 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0002_auto_20211004_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=128),
            preserve_default=False,
        ),
    ]
