# Generated by Django 2.1.5 on 2019-04-10 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EtherSplitApp', '0005_character_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='description',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
    ]