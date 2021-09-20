from __future__ import absolute_import

from django.urls import path, re_path, include
from django.views.generic.list import ListView

from .models import get_active_members
import members.views


urlpatterns = [
    path('',
         ListView.as_view(
             queryset=get_active_members(),
             template_name='members/member_list.html',
        ),
    ),

    path('', include('django.contrib.auth.urls')),

    re_path(r'^valid_user/?$', members.views.valid_user),
    path('history/', members.views.members_history),
    path('collection/', members.views.members_bankcollection_list),
    path('bank/', members.views.members_bank),
    path('bankexport/', members.views.members_bankcollection_sepa),
    path('bankimport/', members.views.members_bankcollection_importjson),
    path('keylist/', members.views.members_key_list),
    path('lazzzorlist/', members.views.members_lazzzor_list),
    path('internlist/', members.views.members_intern_list),

    re_path(r'^(?P<user_username>(\w|-)+)/update/userpic/$', members.views.members_update_userpic),
    re_path(r'^(?P<user_username>(\w|-)+)/update/(?P<update_type>\w+)/$', members.views.members_update),
    re_path(r'^(?P<user_username>(\w|-)+)/$', members.views.members_details),
]
