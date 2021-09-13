#
# Views for issueing announcements to all active members.
#
import smtplib
from datetime import date

from django.shortcuts import render
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
import django.forms as forms
from django.core.mail import send_mail

from members.models import get_active_members, ContactInfo


class AnnouncementForm(forms.Form):
    subject = forms.CharField(required=True, label="Thema", max_length=40)
    body = forms.CharField(required=True, label="Mitteilung",
                           widget=forms.Textarea)
    to = forms.ChoiceField(required=True, label="An",
                           choices=(('collection', 'collection'),
                                    ('keymembers', 'keymembers'),
                                    ('all', 'all'),))


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

@staff_member_required
def announce(request):
    form = AnnouncementForm(request.POST or None)
    if not request.POST or not form.is_valid():
        context = {'form': form, 'user': request.user}
        return render(request, 'announce/write_message.html', context)
    # Valid message: send it!
    users = get_active_members()

    if form.cleaned_data['to'] == 'collection':
        users = _announce_filter_collection(users)
    elif form.cleaned_data['to'] == 'keymembers':
        users = _announce_filter_keymembers(users)

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

        ci = ContactInfo.objects.get(user=user)
        try:
            send_mail(form.cleaned_data['subject'],
                      body,
                      settings.HOS_ANNOUNCE_FROM,
                      [user.email],
                      fail_silently=False)
            ci.last_email_ok = True
            ci.save()
        except smtplib.SMTPException as e:
            f = open(settings.HOS_ANNOUNCE_LOG, 'a')
            f.write('\n\n'+user.email)
            f.write('\n'+repr(e))
            ci.last_email_ok = False
            ci.save()
            f.close()

    context = {'form': form, 'user': request.user, 'users': users}
    return render(request, 'announce/message_sent.html', context)
