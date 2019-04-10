from django.shortcuts import render, get_object_or_404
from EtherSplitApp.models import *


# @login_required(login_url='/login/')
def home(request):
    context = {

    }
    return render(request, 'home.html', context)


def group_characters(request):
    user = User.objects.get(username=request.user.username)
    group = user.groups.get()  # might error if user is in multiple groups
    character_list = Character.objects.filter(is_active=True, user__groups=group).order_by('-name')
    context = {
        'group': group,
        'characters': character_list,
    }
    return render(request, 'characters.html', context)


def character_page(request, character_slug):
    user = User.objects.get(username=request.user.username)
    character = Character.objects.get(slug=character_slug)
    abilities = Ability.objects.filter(character=character)
    weapons = Weapon.objects.filter(character=character)
    items = Item.objects.filter(character=character)
    gear = Gear.objects.filter(character=character)
    spells = Spell.objects.filter(character=character)
    money = Money.objects.filter(character=character)
    # TODO add html pages for each model (ability, weapon, etc.) and insert block into character_page

    context = {
        'user': user,
        'character': character,
        'abilities': abilities,
        'weapons': weapons,
        'items': items,
        'gear': gear,
        'spells': spells,
        'money': money,
    }

    return render(request, 'character_page.html', context)
