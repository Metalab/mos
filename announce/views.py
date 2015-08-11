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
                           choices=(('collection', 'collection'), ('all', 'all'),))


@staff_member_required
def announce(request):
    form = AnnouncementForm(request.POST or None)
    if not request.POST or not form.is_valid():
        context = {'form': form, 'user': request.user}
        return render(request, 'announce/write_message.html', context)
    # Valid message: send it!
    users = get_active_members()
    if form.cleaned_data['to'] != 'all':
        users = users.filter(paymentinfo__bank_collection_allowed=True)\
                     .filter(paymentinfo__bank_collection_mode__id=4)
        for u in users:
            debt = u.contactinfo.get_debt_for_month(date.today())
            if debt == 0:
                users = users.exclude(pk=u.pk)

    for user in users:
        ci = ContactInfo.objects.get(user=user)
        try:
            send_mail(form.cleaned_data['subject'],
                      form.cleaned_data['body'],
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
