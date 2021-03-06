# Generated by Django 2.1.5 on 2019-05-10 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EtherSplitApp', '0022_auto_20190509_2306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Companion',
            fields=[
                ('character_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='EtherSplitApp.Character')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='EtherSplitApp.Character')),
            ],
            bases=('EtherSplitApp.character',),
        ),
    ]
