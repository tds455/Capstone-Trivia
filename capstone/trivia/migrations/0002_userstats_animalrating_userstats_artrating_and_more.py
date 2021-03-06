# Generated by Django 4.0.3 on 2022-04-13 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trivia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstats',
            name='animalrating',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userstats',
            name='artrating',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userstats',
            name='movierating',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userstats',
            name='sportsrating',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userstats',
            name='worldrating',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
