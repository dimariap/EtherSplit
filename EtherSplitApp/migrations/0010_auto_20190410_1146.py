# Generated by Django 2.1.5 on 2019-04-10 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EtherSplitApp', '0009_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]
