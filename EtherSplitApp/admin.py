from django.contrib import admin
from EtherSplitApp.models import *


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'lucky_number', 'hit_points', 'armor', 'initiative', 'is_active', 'is_alive')


class AbilityAdmin(admin.ModelAdmin):
    list_display = ('character', 'name', 'target', 'damage', 'aoe_distance', 'charges', 'turns',
                    'is_super', 'is_active')


class WeaponAdmin(admin.ModelAdmin):
    list_display = ('character', 'name', 'type', 'range', 'damage', 'ammo', 'is_active')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('character', 'name', 'damage', 'aoe_distance', 'charges', 'is_active')


class GearAdmin(admin.ModelAdmin):
    list_display = ('character', 'name', 'hit_points', 'armor', 'is_active')


admin.site.register(Character, CharacterAdmin)
admin.site.register(Ability, AbilityAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Gear, GearAdmin)
