# Generated by Django 2.1.5 on 2019-04-10 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EtherSplitApp', '0010_auto_20190410_1146'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(blank=True, choices=[('str', 'Strength'), ('end', 'Endurance'), ('spd', 'Speed'), ('agi', 'Agility')], max_length=16)),
                ('mind', models.CharField(blank=True, choices=[('int', 'Intelligence'), ('wis', 'Wisdom'), ('cha', 'Charisma'), ('flo', 'Flow')], max_length=16)),
                ('spirit', models.CharField(blank=True, choices=[('lck', 'Luck'), ('mna', 'Mana'), ('wll', 'Will'), ('eng', 'Edgenuity')], max_length=16)),
            ],
        ),
        migrations.AlterModelOptions(
            name='money',
            options={'verbose_name_plural': 'Money'},
        ),
        migrations.AddField(
            model_name='character',
            name='attributes',
            field=models.ManyToManyField(to='EtherSplitApp.Attributes'),
        ),
    ]
