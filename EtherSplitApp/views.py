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
    context = {
        'user': user,
        'character': character,
    }
    return render(request, 'character_page.html', context)
