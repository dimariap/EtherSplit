from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth.models import Group


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # TODO implement a custom user model
    name = models.CharField(max_length=32, unique=True)
    # TODO character stats - mind, body, and spirit
    lucky_number = models.CharField(max_length=3, blank=True, default='')
    hit_points = models.CharField(max_length=5, blank=True, default='')
    armor = models.CharField(max_length=5, blank=True, default='')
    initiative = models.CharField(max_length=3, blank=True, default='')
    # maybe add race/gender or other racial attributes
    description = models.TextField(max_length=500, blank=True, default='')
    # picture = models.ImageField(name=name, width_field=None, height_field=None)
    is_active = models.BooleanField(default=True)  # might add is_hidden for undiscovered characters
    is_alive = models.BooleanField(default=True)  # TODO change to null boolean (for undead)
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Character, self).save(*args, **kwargs)


class Ability(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=32,)
    target = models.CharField(max_length=32, blank=True, choices=(
        ('self', 'Self'),
        ('target', 'Target'),
    ))
    damage = models.CharField(max_length=4, blank=True, default='')
    aoe_radius = models.CharField(max_length=4, blank=True, default='')
    charges = models.CharField(max_length=4, blank=True, default='')
    # TODO add cool down
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
    description = models.TextField(max_length=500, blank=True, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=32,)
    damage = models.CharField(max_length=4, blank=True, default='')
    aoe_radius = models.CharField(max_length=4, blank=True, default='')
    charges = models.CharField(max_length=4, blank=True, default='')
    description = models.TextField(max_length=500, blank=True, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Gear(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=32,)
    hit_points = models.CharField(max_length=5, blank=True, default='')
    armor = models.CharField(max_length=5, blank=True, default='')
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
    damage = models.CharField(max_length=4, blank=True, default='')
    aoe_radius = models.CharField(max_length=4, blank=True, default='')
    mana_cost = models.CharField(max_length=4, blank=True, default='')
    # TODO add cool down
    duration = models.CharField(max_length=4, blank=True, default='', help_text='Number of turns the ability lasts.')
    description = models.TextField(max_length=500, blank=True, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Money(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=6, blank=True, default='')
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
