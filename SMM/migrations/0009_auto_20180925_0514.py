# Generated by Django 2.0 on 2018-09-25 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMM', '0008_auto_20180925_0459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='excluded_keywords',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='optional_keywords',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='required_keywords',
            field=models.TextField(max_length=200, null=True),
        ),
    ]
