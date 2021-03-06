from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.urls import reverse
from EtherSplitApp.models import *
from EtherSplitApp.forms import *
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages


@login_required(login_url='/login/')
def home(request):
    groups = Group.objects.all().order_by('name')
    context = {
        'groups': groups,
    }
    return render(request, 'home.html', context)


@login_required(login_url='/login/')
def all_characters(request):
    npc, created = User.objects.get_or_create(username='NPC', defaults={'username': 'NPC'})
    if created:
        npc.groups.set(Group.objects.all())
        npc.set_password('npc_password')
        npc.save()
        __set_npc_characters_without_a_user(npc)  # sets the characters without a user to npc user
    characters = Character.objects.filter(is_active=True).exclude(user=npc).order_by('name')
    return render(request, 'all_characters.html', {'characters': characters})


@login_required(login_url='/login/')
def group_characters(request, group_id):
    group = Group.objects.get(id=group_id)
    npc, created = User.objects.get_or_create(username='NPC', defaults={'username': 'NPC'})
    if created:
        npc.groups.set(Group.objects.all())
        npc.set_password('npc_password')
        npc.save()
        __set_npc_characters_without_a_user(npc)  # sets the characters without a user to npc user
    character_list = Character.objects.filter(is_active=True, user__groups=group,
                                              companion__isnull=True).exclude(user=npc).order_by('name')
    context = {
        'group': group,
        'characters': character_list,
    }
    return render(request, 'characters.html', context)


@login_required(login_url='/login/')
def character_page(request, character_slug):
    character = Character.objects.get(slug=character_slug)
    character_stats = CharacterStats.objects.filter(character=character)
    abilities = Ability.objects.filter(character=character).order_by('name')
    weapons = Weapon.objects.filter(character=character).order_by('name')
    items = Item.objects.filter(character=character).order_by('name')
    gear = Gear.objects.filter(character=character).order_by('name')
    spells = Spell.objects.filter(character=character).order_by('name')
    money = Money.objects.filter(character=character).order_by('name')
    companions = Companion.objects.filter(master=character).order_by('name')
    if character.name in Companion.objects.values_list('name', flat=True):
        character = Companion.objects.get(slug=character_slug)
    character.armor = __calculate_total_armor(character, gear)

    context = {
        'user': character.user,
        'character': character,
        'character_stats': character_stats,
        'abilities': abilities,
        'weapons': weapons,
        'items': items,
        'gear': gear,
        'spells': spells,
        'money': money,
        'companions': companions,
    }

    return render(request, 'character_page.html', context)


@login_required(login_url='/login/')
def character_gear_page(request, character_slug):
    character = Character.objects.get(slug=character_slug)
    gear = Gear.objects.filter(character=character).order_by('name')
    user = request.user

    context = {
        'character': character,
        'gear': gear,
        'user': user,
    }

    if request.method == 'POST':
        if user == character.user or user.is_staff:
            character_armor = request.POST.get('character_' + str(character.id), None)
            if character_armor and character_armor != character.armor:
                character.armor = character_armor
                character.save(update_fields=['armor'])

            for gear_piece in gear:
                gear_piece_armor = request.POST.get('gear_' + str(gear_piece.id), None)
                if gear_piece_armor and gear_piece_armor != gear_piece.armor:
                    gear_piece.armor = gear_piece_armor
                    gear_piece.save(update_fields=['armor'])

        character_sessions = Session.objects.filter(group=user.groups.get())  # might error if multiple groups
        most_recent_session = character_sessions.latest('date')  # get the most recent session

        return redirect('/sessions/' + str(most_recent_session.id))

    return render(request, 'character_pages/character_gear_page.html', context)


@login_required(login_url='/login/')
def character_hp_page(request, character_slug):
    character = Character.objects.get(slug=character_slug)
    # gear = Gear.objects.filter(character=character)  # uncomment if gear will add HP
    user = request.user

    context = {
        'character': character,
        # 'gear': gear,
        'user': user,
    }

    if request.method == 'POST':
        if user == character.user or user.is_staff:
            character_health_points = request.POST.get('character_' + str(character.id), None)
            if character_health_points and character_health_points != character.health_points:
                character.health_points = character_health_points
                character.save(update_fields=['health_points'])

                # change alive status from health point values
                if int(character.health_points) > 0:
                    character.is_alive = True
                if int(character.health_points) < 0:
                    character.health_points = '0'  # could make negative numbers represent undead
                    character.save(update_fields=['health_points'])
                if int(character.health_points) == 0:
                    character.is_alive = False
                character.save(update_fields=['is_alive'])

            """for gear_piece in gear:
                gear_piece_armor = request.POST.get('gear_' + str(gear_piece.id), None)
                if gear_piece_armor and gear_piece_armor != gear_piece.armor:
                    gear_piece.armor = gear_piece_armor
                    gear_piece.save(update_fields=['armor'])"""

        character_sessions = Session.objects.filter(group=user.groups.get())  # might error if multiple groups
        most_recent_session = character_sessions.latest('date')  # get the most recent session

        return redirect('/sessions/' + str(most_recent_session.id))

    return render(request, 'character_pages/character_hp_page.html', context)


@login_required(login_url='/login/')
def character_ability_page(request, character_slug):
    character = Character.objects.get(slug=character_slug)
    abilities = Ability.objects.filter(character=character).order_by('is_super', 'name')
    user = request.user

    context = {
        'character': character,
        'abilities': abilities,
        'user': user,
    }

    if request.method == 'POST':
        if user == character.user or user.is_staff:
            for ability in abilities:
                print(ability.name)  # subtract 1 (next turn button) from cooldown

        return redirect('/characters/' + str(character.slug) + '/' + 'abilities')

    return render(request, 'character_pages/character_ability_page.html', context)


@login_required(login_url='/login/')
def character_weapon_page(request, character_slug):
    character = Character.objects.get(slug=character_slug)
    weapons = Weapon.objects.filter(character=character).order_by('name')
    user = request.user

    context = {
        'character': character,
        'weapons': weapons,
        'user': user,
    }

    if request.method == 'POST':
        if user == character.user or user.is_staff:
            for weapon in weapons:
                print(weapon.name)  # subtract 1 (next turn button) from cooldown

        return redirect('/characters/' + str(character.slug) + '/' + 'weapons')

    return render(request, 'character_pages/character_weapon_page.html', context)


@login_required(login_url='/login/')
def character_spells_page(request, character_slug):
    character = Character.objects.get(slug=character_slug)
    spells = Spell.objects.filter(character=character).order_by('name')
    user = request.user

    context = {
        'character': character,
        'spells': spells,
        'user': user,
    }

    if request.method == 'POST':
        if user == character.user or user.is_staff:
            for spell in spells:
                print(spell.name)  # subtract 1 (next turn button) from cooldown

        return redirect('/characters/' + str(character.slug) + '/' + 'spells')

    return render(request, 'character_pages/character_spells_page.html', context)


@login_required(login_url='/login/')
def rules(request):
    admin_rule_list = Rule.objects.all()
    user_rule_list = Rule.objects.filter(for_gm_only=False)
    # might list user twice for GM
    context = {
        'admin_rules': admin_rule_list,
        'user_rules': user_rule_list,
        'user': request.user,
    }

    return render(request, 'rules.html', context)


@login_required(login_url='/login/')
def sessions(request):
    user = User.objects.get(username=request.user.username)
    session_list = Session.objects.all().order_by('-date')

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
    characters = Character.objects.filter(user__groups=session.group).order_by('-initiative', 'name')
    user = request.user

    for character in characters:
        gear = Gear.objects.filter(character=character)
        character.armor = __calculate_total_armor(character, gear)

    context = {
        'session': session,
        'characters': characters,
        'user': user,
    }

    if request.method == 'POST':
        is_admin_page = request.POST.get('is-admin-page', False)

        if user.is_staff and is_admin_page:
            is_active_list = request.POST.getlist('is-active-list', None)
            is_alive_list = request.POST.getlist('is-alive-list', None)
            __update_active_statuses(session, is_active_list)
            __update_alive_statuses(session, is_alive_list)

        # start_next_turn = request.POST.get('start-next-turn', False)

        for character in characters:
            if user == character.user or user.is_staff:
                if not character.initiative:
                    initiative = request.POST.get(str(character.id) + '_initiative', '')
                    character.initiative = initiative
                    character.save(update_fields=['initiative'])

        return redirect('/sessions/' + str(session_id))

    return render(request, 'session_page.html', context)


# authentication views
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            messages.warning(request, 'Unable to login, please try again.')

        return HttpResponseRedirect('/')

    return render(request, 'login.html')


def signout(request):
    logout(request)
    return redirect(signin)


def handler404(request, *args, **kwargs):
    return render(request, '404.html', status=404)


def handler500(request, *args, **kwargs):
    return render(request, '500.html', status=500)


# methods
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
            character.save(update_fields=['initiative'])


def __update_active_statuses(session, is_active_list):
    if is_active_list is None:
        return

    is_active_list = list(map(int, is_active_list))  # convert strings to ints
    users = User.objects.filter(groups=session.group)
    for user in users:
        characters = Character.objects.filter(user=user)
        for character in characters:
            if character.id in is_active_list:
                character.is_active = True
            else:
                character.is_active = False
            character.save(update_fields=['is_active'])


def __update_alive_statuses(session, is_alive_list):
    if is_alive_list is None:
        return

    is_alive_list = list(map(int, is_alive_list))  # convert strings to ints
    users = User.objects.filter(groups=session.group)
    for user in users:
        characters = Character.objects.filter(user=user)
        for character in characters:
            if character.id in is_alive_list:
                character.is_alive = True
            else:
                character.is_alive = False
            character.save(update_fields=['is_alive'])


def __set_npc_characters_without_a_user(npc):
    characters_without_user = User.objects.filter(username__isnull=True)
    for character in characters_without_user:
        character.user = npc
        character.save(update_files=['user'])