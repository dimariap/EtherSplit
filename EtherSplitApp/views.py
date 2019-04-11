from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.urls import reverse

from EtherSplitApp.models import *
from EtherSplitApp.forms import *
from django.contrib.admin.views.decorators import staff_member_required


@login_required(login_url='/login/')
def home(request):
    context = {

    }
    return render(request, 'home.html', context)


@login_required(login_url='/login/')
def group_characters(request):
    user = User.objects.get(username=request.user.username)
    group = user.groups.get()  # might error if user is in multiple groups
    character_list = Character.objects.filter(is_active=True, user__groups=group).order_by('-name')
    context = {
        'group': group,
        'characters': character_list,
    }
    return render(request, 'characters.html', context)


@login_required(login_url='/login/')
def character_page(request, character_slug):
    user = User.objects.get(username=request.user.username)
    character = Character.objects.get(slug=character_slug)
    abilities = Ability.objects.filter(character=character)
    weapons = Weapon.objects.filter(character=character)
    items = Item.objects.filter(character=character)
    gear = Gear.objects.filter(character=character)
    spells = Spell.objects.filter(character=character)
    money = Money.objects.filter(character=character)

    character.armor = __calculate_total_armor(character, gear)

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


@login_required(login_url='/login/')
def rules(request):
    rule_list = Rule.objects.all()

    return render(request, 'rules.html', {'rules': rule_list})


@login_required(login_url='/login/')
def sessions(request):
    user = User.objects.get(username=request.user.username)
    group = user.groups.get()  # might error if user is in multiple groups
    session_list = Session.objects.filter(group=group).order_by('-date')

    context = {
        'sessions': session_list,
        'user': user,
    }

    return render(request, 'sessions.html', context)


@staff_member_required(login_url='/login/')
def new_session(request):
    groups = Group.objects.all().order_by('name')

    if request.method == 'POST':
        # TODO give message if form is invalid
        form = NewSessionForm(request.POST)

        if form.is_valid():
            form.name = request.POST.get('name', '')
            group_id = request.POST.get('group', '')
            form.group = Group.objects.get(id=group_id)
            form.description = request.POST.get('description', '')
            new_created_session = form.save()

            __reset_all_session_initiatives(new_created_session)

            return HttpResponseRedirect(reverse(session_page, args=(new_created_session.pk,)))

    return render(request, 'new_session.html', {'groups': groups})


@login_required(login_url='/login/')
def session_page(request, session_id):
    session = Session.objects.get(id=session_id)
    # characters = __get_session_characters(session)
    users = User.objects.get(groups=session.group)
    characters = Character.objects.filter(user=users).order_by('-initiative', 'name')
    # TODO add 'is_killed' buttons and strike-through the character

    for character in characters:
        gear = Gear.objects.filter(character=character)
        character.armor = __calculate_total_armor(character, gear)

    context = {
        'session': session,
        'characters': characters,
    }
    return render(request, 'session_page.html', context)


def __calculate_total_armor(character, gear):
    total_char_armor = character.armor

    if total_char_armor.isdigit():
        total_char_armor = int(total_char_armor)

        for gear_piece in gear:
            if gear_piece.armor.isdigit():
                total_char_armor += int(gear_piece.armor)

    return total_char_armor


def __reset_all_session_initiatives(session):
    users = User.objects.filter(groups=session.group)
    for user in users:
        characters = Character.objects.filter(user=user)
        for character in characters:
            character.initiative = ''
            character.save()
