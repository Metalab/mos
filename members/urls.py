from django.conf.urls.defaults import *

from mos.members.models import *


info_dict = {
    'queryset': get_active_members(),
    'template_name': 'members/member_list.html',
}

urlpatterns = patterns('',
    (r'^login/?$', 'django.contrib.auth.views.login',
     {'template_name': 'members/member_login.html'}),
    (r'^logout/?$', 'django.contrib.auth.views.logout',),
    (r'^valid_user/?$', 'mos.members.views.valid_user',),

    (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    (r'^history/$', 'mos.members.views.members_history'),
    (r'^change_password/$', 'django.contrib.auth.views.password_change',
     {'template_name': 'members/member_update_password.html'}),
    (r'^change_password/done/$',
     'django.contrib.auth.views.password_change_done',
     {'template_name': 'members/member_update_password_done.html'}),
    (r'^collection/$', 'mos.members.views.members_bankcollection_list'),
    (r'^keylist/$', 'mos.members.views.members_key_list'),
    (r'^lazzzorlist/$', 'mos.members.views.members_lazzzor_list'),
    (r'^(?P<user_username>(\w|-)+)/update/userpic/$',
     'mos.members.views.members_update_userpic'),
    (r'^(?P<user_username>(\w|-)+)/update/(?P<update_type>\w+)/$',
     'mos.members.views.members_update'),
    (r'^(?P<user_username>(\w|-)+)/$', 'mos.members.views.members_details'),
)
