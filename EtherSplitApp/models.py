from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth.models import Group


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # TODO implement a custom user model
    name = models.CharField(max_length=32, unique=True)
    lucky_number = models.CharField(max_length=3, blank=True, default='')
    health_points = models.CharField(max_length=8, blank=True, default='')
    armor = models.CharField(max_length=8, blank=True, default='')
    initiative = models.CharField(max_length=3, blank=True, default='')
    # maybe add race/gender or other racial attributes
    description = models.TextField(max_length=500, blank=True, default='')
    # picture = models.ImageField(name=name, width_field=None, height_field=None)
    is_active = models.BooleanField(default=True)  # might add is_hidden for undiscovered characters
    is_alive = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Character, self).save(*args, **kwargs)


class CharacterStats(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    str = models.CharField(max_length=4, blank=True, default='', help_text='Strength')
    end = models.CharField(max_length=4, blank=True, default='', help_text='Endurance')
    agi = models.CharField(max_length=4, blank=True, default='', help_text='Agility')
    spd = models.CharField(max_length=4, blank=True, default='', help_text='Speed')
    cog = models.CharField(max_length=4, blank=True, default='', help_text='Cognition')
    wis = models.CharField(max_length=4, blank=True, default='', help_text='Wisdom')
    mag = models.CharField(max_length=4, blank=True, default='', help_text='Magnetism')
    flo = models.CharField(max_length=4, blank=True, default='', help_text='Flow')
    luk = models.CharField(max_length=4, blank=True, default='', help_text='Luck')
    wil = models.CharField(max_length=4, blank=True, default='', help_text='Will')
    chi = models.CharField(max_length=4, blank=True, default='', help_text='Chi')
    syn = models.CharField(max_length=4, blank=True, default='', help_text='Syncro')

    def __str__(self):
        return self.character.name

    class Meta:
        verbose_name_plural = 'Character Stats'


class Ability(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=32,)
    target = models.CharField(max_length=32, blank=True, choices=(
        ('self', 'Self'),
        ('target', 'Target'),
    ))
    damage = models.CharField(max_length=8, blank=True, default='')
    aoe_radius = models.CharField(max_length=8, blank=True, default='')
    charges = models.CharField(max_length=8, blank=True, default='')
    cooldown = models.CharField(max_length=8, blank=True, default='', choices=(
                                    ('0', 'Instant'),
                                    ('1', '1 Turn'),
                                    ('2', '2 Turns'),
                                    ('3', '3 Turns'),
                                    ('4', '4 Turns'),
                                    ('5', '5 Turns'),
                                ))
    # TODO add if critical condition
    duration = models.CharField(max_length=8, blank=True, default='', help_text='Number of turns the ability lasts.',
                                choices=(
                                    ('instant', 'Instant'),
                                    ('1turn', '1 Turn'),
                                    ('2turn', '2 Turns'),
                                    ('3turn', '3 Turns'),
                                    ('4turn', '4 Turns'),
                                    ('5turn', '5 Turns'),
                                ))
    description = models.TextField(max_length=500, blank=True, default='')
    is_super = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Abilities'


class Weapon(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=32,)
    type = models.CharField(max_length=32, blank=True, default='')
    range = models.CharField(max_length=32, blank=True, default='')
    damage = models.CharField(max_length=8, blank=True, default='')
    ammo = models.CharField(max_length=8, blank=True, default='', help_text='Put \'melee\' if melee weapon.')
    description = models.TextField(max_length=500, blank=True, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=32,)
    damage = models.CharField(max_length=8, blank=True, default='')
    aoe_radius = models.CharField(max_length=8, blank=True, default='')
    charges = models.CharField(max_length=8, blank=True, default='')
    description = models.TextField(max_length=500, blank=True, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Gear(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=32,)
    health_points = models.CharField(max_length=8, blank=True, default='')
    armor = models.CharField(max_length=8, blank=True, default='')
    body_part = models.CharField(max_length=12, blank=True, default='', choices=(
        ('head', 'Head'),
        ('chest', 'Chest'),
        ('left_arm', 'Left Arm'),
        ('right_arm', 'Right Arm'),
        ('arms', 'Arms'),
        ('waist', 'Waist'),
        ('left_leg', 'Left Leg'),
        ('right_leg', 'Right Leg'),
        ('legs', 'legs'),
        ('hands', 'Hands'),
        ('feet', 'Feet'),
    ))
    description = models.TextField(max_length=500, blank=True, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Gear'


class Spell(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=32,)
    target = models.CharField(max_length=32, blank=True, choices=(
        ('self', 'Self'),
        ('target', 'Target'),
    ))
    damage = models.CharField(max_length=8, blank=True, default='')
    aoe_radius = models.CharField(max_length=8, blank=True, default='')
    mana_cost = models.CharField(max_length=8, blank=True, default='')
    # TODO add cool down
    duration = models.CharField(max_length=8, blank=True, default='', help_text='Number of turns the ability lasts.')
    description = models.TextField(max_length=500, blank=True, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Money(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=8, blank=True, default='')
    currency = models.CharField(max_length=32, blank=True, choices=(
        ('holla', 'Holla'),
        ('shi', 'Shi'),
        ('credit-stick', 'Credit Stick'),
    ))

    def __str__(self):
        return "{} {} {}".format(self.character, self.quantity, self.currency)

    class Meta:
        verbose_name_plural = 'Money'

# TODO add companion class (define rules first)


class Rule(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    for_gm_only = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Session(models.Model):
    name = models.CharField(max_length=64)
    date = models.DateField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)
    description = models.TextField(max_length=500, blank=True, default='')

    def __str__(self):
        return self.name
