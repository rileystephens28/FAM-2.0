# Generated by Django 2.0 on 2018-03-16 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='price',
        ),
        migrations.AlterField(
            model_name='stock',
            name='ask',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='bid',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='last',
            field=models.FloatField(default=None, null=True),
        ),
    ]