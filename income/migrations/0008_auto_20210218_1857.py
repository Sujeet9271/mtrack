# Generated by Django 3.1.5 on 2021-02-18 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0007_auto_20210217_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='income',
            field=models.IntegerField(default=0, verbose_name='Income'),
        ),
    ]
