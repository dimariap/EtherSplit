from django.db import models
from django.contrib.auth.models import User


class Character(models.Model):
    user = User
    name = models.CharField(max_length=32, unique=True)
    hit_points = models.CharField(max_length=5, blank=True, default='')
    armor = models.CharField(max_length=5, blank=True, default='')
    initiative = models.CharField(max_length=3, blank=True, default='')
    is_active = models.BooleanField(default=True)
    is_alive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Ability(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=32,)
    target = models.CharField(max_length=32, choices=(
        ('self', 'Self'),
        ('target', 'Target'),
    ))
    damage = models.CharField(max_length=4, blank=True, default='')
    aoe_distance = models.CharField(max_length=4, blank=True, default='')
    charges = models.CharField(max_length=4, blank=True, default='')
    turns = models.CharField(max_length=4, blank=True, default='', help_text='Number of turns the ability lasts.')
    description = models.TextField(max_length=500)
    is_super = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Weapon(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=32,)
    type = models.CharField(max_length=32, blank=True, default='')  # TODO add choices like Sword, Gun, etc.
    range = models.CharField(max_length=32, choices=(
        ('short', 'Short'),
        ('short-medium', 'Short to Medium'),
        ('medium', 'Medium'),
        ('medium-long', 'Medium to Long'),
        ('long', 'Long'),
        ('unknown', 'Unknown')
    ))
    damage = models.CharField(max_length=4, blank=True, default='')
    ammo = models.CharField(max_length=5, blank=True, default='', help_text='Put \'melee\' if melee weapon.')
    description = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=32,)
    damage = models.CharField(max_length=4, blank=True, default='')
    aoe_distance = models.CharField(max_length=4, blank=True, default='')
    charges = models.CharField(max_length=4, blank=True, default='')
    description = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Gear(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=32,)
    hit_points = models.CharField(max_length=5, blank=True, default='')
    armor = models.IntegerField(max_length=5, blank=True, default='')
    description = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
