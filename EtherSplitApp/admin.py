from django.contrib import admin
from EtherSplitApp.models import *


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'lucky_number', 'health_points', 'armor', 'initiative', 'is_active', 'is_alive')


class CharacterStatsAdmin(admin.ModelAdmin):
    pass


class AbilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'character', 'target', 'damage', 'aoe_radius', 'charges', 'duration',
                    'is_super', 'is_active')


class WeaponAdmin(admin.ModelAdmin):
    list_display = ('name', 'character', 'type', 'range', 'damage', 'ammo', 'is_active')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'character', 'damage', 'aoe_radius', 'charges', 'is_active')


class GearAdmin(admin.ModelAdmin):
    list_display = ('name', 'character', 'health_points', 'armor', 'is_active')


class SpellAdmin(admin.ModelAdmin):
    list_display = ('name', 'character', 'target', 'damage', 'aoe_radius', 'mana_cost', 'duration', 'is_active')


class MoneyAdmin(admin.ModelAdmin):
    list_display = ('character', 'quantity', 'currency')


class CompanionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'health_points', 'armor', 'initiative', 'is_active', 'is_alive')


class RuleAdmin(admin.ModelAdmin):
    pass


class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')


admin.site.register(Character, CharacterAdmin)
admin.site.register(CharacterStats, CharacterStatsAdmin)
admin.site.register(Ability, AbilityAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Gear, GearAdmin)
admin.site.register(Spell, SpellAdmin)
admin.site.register(Money, MoneyAdmin)
admin.site.register(Companion, CompanionAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(Session, SessionAdmin)
