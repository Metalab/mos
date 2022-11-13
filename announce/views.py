#
# Views for issueing announcements to all active members.
#
from functools import partial
from datetime import date, datetime

from django.shortcuts import render
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
import django.forms as forms
from django.db.models import Q

from members.models import get_active_members, ContactInfo, KindOfMembership


def _announce_filter_collection(users):
    users = users.filter(paymentinfo__bank_collection_allowed=True) \
                    .filter(paymentinfo__bank_collection_mode__id=4)
    for u in users:
        debt = u.contactinfo.get_debt_for_month(date.today())
        if debt == 0:
            users = users.exclude(pk=u.pk)
    return users

def _announce_filter_keymembers(users):
    return users.filter(contactinfo__has_active_key=True) \
                    .exclude(contactinfo__key_id=None)


def _announce_filter_fee_category_members(users, fee_category):
    return users.filter(
        Q(membershipperiod__begin__lt=datetime.now()) &
        (Q(membershipperiod__end__isnull=True) | Q(membershipperiod__end__gt=datetime.now())) &
        Q(membershipperiod__kind_of_membership__fee_category=fee_category)
    )


ANNOUNCE_TARGETS = {
    'collection': ('collection', _announce_filter_collection),
    'keymembers': ('keymembers', _announce_filter_keymembers),
    **{
        cat[0]: (cat[1] + ' members', partial(_announce_filter_fee_category_members, fee_category=cat[0]))
        for cat in KindOfMembership.FEE_CATEGORY
    },
    'all': ('all', lambda users: users),
}

class AnnouncementForm(forms.Form):
    subject = forms.CharField(required=True, label="Thema", max_length=40)
    body = forms.CharField(required=True, label="Mitteilung",
                           widget=forms.Textarea)
    to = forms.ChoiceField(required=True, label="An", choices=((k, v[0]) for k, v in ANNOUNCE_TARGETS.items()))


@staff_member_required
def announce(request):
    form = AnnouncementForm(request.POST or None)
    if not request.POST or not form.is_valid():
        context = {'form': form, 'user': request.user}
        return render(request, 'announce/write_message.html', context)
    # Valid message: send it!
    users = get_active_members()

    users = ANNOUNCE_TARGETS[form.cleaned_data['to']][1](users)

    for user in users:
        body = form.cleaned_data['body'] \
            .replace('{{username}}', user.get_username()) \
            .replace('{{full_name}}', user.get_full_name()) \
            .replace('{{short_name}}', user.get_short_name()) \
            .replace('{{first_name}}', user.first_name) \
            .replace('{{last_name}}', user.last_name) \
            .replace('{{user_id}}', str(user.pk)) \
            .replace('{{profile_link}}',
                f'https://{settings.SESSION_COOKIE_DOMAIN}/member/{user.get_username()}/') \
            .replace('{{IBAN}}', str(settings.HOS_SEPA_CREDITOR_IBAN)) \
            .replace('{{BIC}}', str(settings.HOS_SEPA_CREDITOR_BIC))

        user.contactinfo.send_mail(form.cleaned_data['subject'], body, settings.HOS_ANNOUNCE_LOG)

    context = {'form': form, 'user': request.user, 'users': users}
    return render(request, 'announce/message_sent.html', context)
