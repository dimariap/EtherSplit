from django.contrib import admin
from EtherSplitApp.models import *


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')


admin.site.register(Character, CharacterAdmin)
