# Generated by Django 2.2.4 on 2023-01-17 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0001_initial'),
        ('pie_app', '0003_auto_20230117_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='pie',
        ),
        migrations.AddField(
            model_name='vote',
            name='pie',
            field=models.ManyToManyField(related_name='voted_pies', to='pie_app.Pypie'),
        ),
        migrations.RemoveField(
            model_name='vote',
            name='user',
        ),
        migrations.AddField(
            model_name='vote',
            name='user',
            field=models.ManyToManyField(related_name='voted_users', to='login_app.User'),
        ),
    ]