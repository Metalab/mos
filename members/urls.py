from __future__ import absolute_import

from django.conf.urls import *
from django.views.generic.list import ListView

from .models import get_active_members


urlpatterns = patterns('',
    url(r'^login/?$', 'django.contrib.auth.views.login', {'template_name': 'members/member_login.html'}, name='login'),
    url(r'^logout/?$', 'django.contrib.auth.views.logout', name='logout'),
    (r'^valid_user/?$', 'members.views.valid_user',),

    (r'^$', ListView.as_view(queryset=get_active_members(), template_name='members/member_list.html')),
    (r'^history/$', 'members.views.members_history'),
    url(r'^change_password/$', 'django.contrib.auth.views.password_change', {'template_name': 'members/member_update_password.html'}, name='password_change'),
    url(r'^change_password/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'members/member_update_password_done.html'}, name='password_change_done'),
    (r'^collection/$', 'members.views.members_bankcollection_list'),
    (r'^keylist/$', 'members.views.members_key_list'),
    (r'^lazzzorlist/$', 'members.views.members_lazzzor_list'),
    (r'^(?P<user_username>(\w|-)+)/update/userpic/$', 'members.views.members_update_userpic'),
    (r'^(?P<user_username>(\w|-)+)/update/(?P<update_type>\w+)/$', 'members.views.members_update'),
    (r'^(?P<user_username>(\w|-)+)/$', 'members.views.members_details'),
)
