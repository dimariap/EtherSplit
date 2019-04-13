"""EtherSplit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from EtherSplitApp.views import *

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^sessions/$', sessions, name='sessions'),
    url(r'^sessions/new-session/$', new_session, name='new_session'),
    url(r'^sessions/(?P<session_id>\d+)/$', session_page, name='session_page'),
    url(r'^rules/$', rules, name='rules'),
    url(r'^characters/$', group_characters, name='group_characters'),
    url(r'^characters/(?P<character_slug>[\w-]+)/$', character_page, name='character_page'),
    url(r'^characters/(?P<character_slug>[\w-]+)/gear$', character_gear_page, name='character_gear_page'),
    # authentication urls
    url(r'^login/$', signin),
    url(r'^logout/$', signout),
    # path(r'^password_reset/$', password_reset, name='password_reset'),
    # path(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
    # path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        # password_reset_confirm, name='password_reset_confirm'),
    # path(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),
]

handler404 = handler404
handler500 = handler500
