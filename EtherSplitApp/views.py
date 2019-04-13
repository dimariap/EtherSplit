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
def character_gear_page(request, character_slug):
    character = Character.objects.get(slug=character_slug)
    gear = Gear.objects.filter(character=character)
    user = request.user

    context = {
        'character': character,
        'gear': gear,
        'user': user,
    }

    if request.method == 'POST':
        if user == character.user or user.is_staff:
            for gear_piece in gear:
                gear_piece_armor = request.POST.get(str(gear_piece.id), None)
                if gear_piece_armor and gear_piece_armor != gear_piece.armor:
                    gear_piece.armor = gear_piece_armor
                    gear_piece.save()

        return redirect('/characters/' + str(character.slug) + '/' + 'gear')

    return render(request, 'character_gear_page.html', context)


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
    users = User.objects.get(groups=session.group)
    characters = Character.objects.filter(user=users).order_by('-initiative', 'name')

    for character in characters:
        gear = Gear.objects.filter(character=character)
        character.armor = __calculate_total_armor(character, gear)

    context = {
        'session': session,
        'characters': characters,
        'user': request.user,
    }  # TODO is not intiaitaive input, else display

    if request.method == 'POST':
        is_active_list = request.POST.getlist('is-active-list', None)
        is_alive_list = request.POST.getlist('is-alive-list', None)
        __update_active_statuses(session, is_active_list)
        __update_alive_statuses(session, is_alive_list)

        for character in characters:
            if not character.initiative:
                initiative = request.POST.get(str(character.id) + '_initiative', '')
                character.initiative = initiative
                print(initiative)
                character.save()

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
            character.save()


def __update_active_statuses(session, is_active_list):
    if not is_active_list:
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
            character.save()


def __update_alive_statuses(session, is_alive_list):
    if not is_alive_list:
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
            character.save()
