# Generated by Django 2.1 on 2019-12-21 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_auto_20191222_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policyrule',
            name='uid',
            field=models.IntegerField(unique=True),
        ),
    ]