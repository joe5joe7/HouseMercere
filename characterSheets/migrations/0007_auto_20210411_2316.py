# Generated by Django 3.1.7 on 2021-04-12 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characterSheets', '0006_auto_20210409_2231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spell',
            name='level',
        ),
        migrations.AddField(
            model_name='spell',
            name='base',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='spell',
            name='other',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
