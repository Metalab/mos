from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.generic.list import ListView

import members.views

from .models import get_active_members

username_patterns = [
    path(r'update/userpic/', members.views.members_update_userpic),
    re_path(r'^update/(?P<update_type>\w+)/$', members.views.members_update),
    path('', members.views.members_details),
]

urlpatterns = [
    path('',
         ListView.as_view(
             queryset=get_active_members().prefetch_related("contactinfo"),
             template_name='members/member_list.html',
        ),
    ),

    path('', include('django.contrib.auth.urls')),

    re_path(r'^valid_user/?$', members.views.valid_user),
    path('history/', members.views.members_history),
    path('hetti/', members.views.hetti),
    path('bank/', members.views.members_bank),
    path('bank/json/import', members.views.members_bank_json_import),
    path('bank/json/match', members.views.members_bank_json_match),
    path('keylist/', members.views.members_key_list),
    path('internlist/', members.views.members_intern_list),

    re_path(r'^(?P<user_username>([\w\-+.@_])+)/', include(username_patterns)),
]
