# Generated by Django 2.0 on 2018-09-12 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SMM', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StatusID', models.CharField(max_length=45)),
                ('Content', models.TextField()),
                ('CreatedAt', models.DateTimeField()),
                ('ResharerCount', models.IntegerField()),
                ('Source', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='PostUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserID', models.CharField(max_length=60)),
                ('DisplayName', models.CharField(max_length=45)),
                ('DisplayImage', models.CharField(max_length=1024)),
                ('TotalLikes', models.IntegerField(blank=True, default=None, null=True)),
                ('TotalPosts', models.IntegerField(blank=True, default=None, null=True)),
                ('FollowingCount', models.IntegerField(blank=True, default=None, null=True)),
                ('FollowerCount', models.IntegerField(blank=True, default=None, null=True)),
                ('PostReshareCount', models.IntegerField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resharer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SMM.Post')),
                ('PostUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SMM.PostUser')),
            ],
        ),
        migrations.RemoveField(
            model_name='keyword',
            name='alert_name',
        ),
        migrations.RemoveField(
            model_name='keyword',
            name='excluded_keywords',
        ),
        migrations.RemoveField(
            model_name='keyword',
            name='optional_keywords',
        ),
        migrations.RemoveField(
            model_name='keyword',
            name='required_keywords',
        ),
        migrations.AddField(
            model_name='keyword',
            name='Excluded',
            field=models.CharField(blank=True, default=None, max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='keyword',
            name='Optional',
            field=models.CharField(blank=True, default=None, max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='keyword',
            name='Required',
            field=models.CharField(blank=True, default=None, max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='keyword',
            name='Text',
            field=models.CharField(default='pepsi', max_length=45),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='Keyword',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SMM.Keyword'),
        ),
        migrations.AddField(
            model_name='post',
            name='PostUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SMM.PostUser'),
        ),
    ]
