# Generated by Django 2.1.5 on 2019-04-11 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EtherSplitApp', '0013_auto_20190410_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='for_gm_only',
            field=models.BooleanField(default=False),
        ),
    ]