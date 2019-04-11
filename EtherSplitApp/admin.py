from django.contrib import admin
from EtherSplitApp.models import *


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'lucky_number', 'hit_points', 'armor', 'initiative', 'is_active', 'is_alive')


class AbilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'character', 'target', 'damage', 'aoe_radius', 'charges', 'duration',
                    'is_super', 'is_active')


class WeaponAdmin(admin.ModelAdmin):
    list_display = ('name', 'character', 'type', 'range', 'damage', 'ammo', 'is_active')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'character', 'damage', 'aoe_radius', 'charges', 'is_active')


class GearAdmin(admin.ModelAdmin):
    list_display = ('name', 'character', 'hit_points', 'armor', 'is_active')


class SpellAdmin(admin.ModelAdmin):
    list_display = ('name', 'character', 'target', 'damage', 'aoe_radius', 'mana_cost', 'duration', 'is_active')


class MoneyAdmin(admin.ModelAdmin):
    list_display = ('character', 'quantity', 'currency')


class RuleAdmin(admin.ModelAdmin):
    pass


class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')


admin.site.register(Character, CharacterAdmin)
admin.site.register(Ability, AbilityAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Gear, GearAdmin)
admin.site.register(Spell, SpellAdmin)
admin.site.register(Money, MoneyAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(Session, SessionAdmin)
