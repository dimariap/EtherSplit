from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from EtherSplitApp.models import *
from EtherSplitApp.forms import *


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
    session_list = Session.objects.filter(group=group)

    context = {
        'sessions': session_list,
    }

    return render(request, 'sessions.html', context)


def new_session(request):
    groups = Group.objects.all().order_by('name')
    form_class = NewSessionForm

    if request.method == 'POST':
        # TODO redirect to new session
        # TODO give message if form is invalid
        form = form_class(data=request.POST)

        if form.is_valid():
            session_name = request.POST.get('session_name', '')
            session_group = request.POST.get('session_group', '')
            session_description = request.POST.get('session_description', '')

            print(session_name)
            print(session_group)
            print(session_description)

    return render(request, 'new_session.html', {'groups': groups})


def session_page(request, session_id):
    session = Session.objects.get(id=session_id)
    context = {
        'session': session
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
