# Generated by Django 2.0 on 2018-09-19 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMM', '0002_auto_20180919_0530'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='Sentiment',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='profile',
            table='Profile',
        ),
    ]
