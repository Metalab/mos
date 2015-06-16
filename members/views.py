from datetime import *

from dateutil.rrule import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings

from mos.members.forms import UserEmailForm, UserNameForm, UserAdressForm,\
                              UserImageForm, UserInternListForm
from mos.members.models import *
from mos.members.util import *
from django.contrib.auth import authenticate


def members_history(request):
    history_entry_list = get_list_of_history_entries()
    history_list = []
    months = list(rrule(MONTHLY, dtstart=date(2006, 3, 1), until=date.today()))
    for dt in months:
        history_list.append(history_entry_list[dt.date()])
    history_list.reverse()
    return render_to_response('members/members_history.html',
                              {'list': history_list},
                              context_instance=RequestContext(request))

@csrf_exempt
def valid_user(request):
    # #tyrsystem
    # I'm no sure what this comment means... "Tuer-System"? I've found entries
    # in Apache's log file no younger than a year. Probably this is not used
    # anymore.
    if not request.is_secure():
        raise Http404()
    user_cache = authenticate(
            username=request.POST.get('user'),
            password=request.POST.get('pass')
        )
    if user_cache and user_cache.is_active:
        return HttpResponse('OK')
    return HttpResponse('FAIL', status=403)


def members_details(request, user_username, errors="", update_type=""):
    editable = False
    if request.user.username == user_username:
        editable = True
    user = get_object_or_404(User, username = user_username)
    return render_to_response('members/members_details.html',
                              {'item': user,
                               'ea': editable,
                               'error_form': errors,
                               'error_type': update_type,
                               }, context_instance=RequestContext(request))


def members_update(request, user_username, update_type):
    if not request.POST or not request.user.username == user_username:
        return members_details(request, user_username,
                               "no permission to edit settings", "permission")
    user = get_object_or_404(User, username = user_username)

    error_form = False
    error_type = False

    if update_type == "email" and request.method == "POST":
        update_form = UserEmailForm(request.POST, instance=user)

    elif update_type == "name" and request.method == "POST":
        update_form = UserNameForm(request.POST, instance=user)

    elif update_type == "adress" and request.method == "POST":
        contact_info = get_object_or_404(ContactInfo, user=user)
        update_form = UserAdressForm(request.POST, instance=contact_info)

    elif update_type == "internlist" and request.method == "POST":
        contact_info = get_object_or_404(ContactInfo, user=user)
        update_form = UserInternListForm(request.POST, instance=contact_info)

    if update_form.is_valid():
        update_form.save()
    else:
        error_form = update_form
        error_type = update_type

    return members_details(request, user_username, error_form, error_type)


@login_required
def members_bankcollection_list(request):
    if request.user.is_superuser:
        # get members that are active and have monthly collection activated
        members_to_collect_from = get_active_members()\
                                  .filter(paymentinfo__bank_collection_allowed=True)\
                                  .filter(paymentinfo__bank_collection_mode__id=4)
                                    # 4 = monthly


        # build a list of collection records with name, bank data, amount
        # and a description
        collection_records = []

        for m in members_to_collect_from:
            debt = m.contactinfo.get_debt_for_month(date.today())
            if debt != 0:
                pmi = m.paymentinfo
                # on the first debit initiation, set the mandate signing date
                if not pmi.bank_account_date_of_signing:
                    pmi.bank_account_date_of_signing = date.today()
                    pmi.save()
                ci = m.contactinfo
                collection_records.append([m.first_name, m.last_name,
                                           pmi.bank_account_number,
                                           pmi.bank_code,
                                           pmi.bank_account_owner,
                                           str(debt),
                                           'Mitgliedsbeitrag %d/%d'
                                           %(date.today().year, date.today()\
                                                                .month),
                                           pmi.bank_account_iban or '',
                                           pmi.bank_account_bic or '',
                                           pmi.bank_account_mandate_reference or '',
                                           pmi.bank_account_date_of_signing.isoformat(),
                                           'RCUR', # FIXME: should be "FRST" on initial run
                                           settings.HOS_SEPA_CREDITOR_ID,
                                           ])

        #format as csv and return it
        csv = '\r\n'.join([';'.join(x) for x in collection_records])

        return HttpResponse(csv, content_type='text/plain; charset=utf-8')


    else:
        return HttpResponseNotAllowed('you are not allowed to use this method')

def members_key_list(request):
    #get active members with active keys
    members_with_keys = get_active_and_future_members().filter(contactinfo__has_active_key=True)
    #return HttpResponse("blah", content_type='text/plain')

    #just output keys one line per key
    text = '\r\n'.join([x.contactinfo.key_id for x in members_with_keys])
    return HttpResponse(text, content_type='text/plain')

def members_lazzzor_list(request):
    """
    Returns key ids and usernames of members with lazzzor privileges as
    comma separated list."""
    members_with_privs = get_active_and_future_members().filter(
                             contactinfo__has_lazzzor_privileges=True)
    result = ['%s,%s,%s' % (m.contactinfo.key_id, m.username,
                            m.contactinfo.lazzzor_rate)
                  for m in members_with_privs]
    return HttpResponse('\r\n'.join(result), content_type='text/plain')

def members_update_userpic(request, user_username):
    if not request.user.username == user_username:
        return members_details(request, user_username,
                               "no permission to edit settings", "permission")

    if request.method == "POST":
        user = get_object_or_404(User, username = user_username)
        contact_info = get_object_or_404(ContactInfo, user=user)
        image_form=UserImageForm(request.POST, request.FILES,
                                 instance=contact_info)
        if image_form.is_valid():
            image_data = image_form.save()
            image_data.save()
            #return to userpage if upload was successfull
            return members_details(request, user_username)
    else:
        image_form=UserImageForm()

    return render_to_response('members/member_update_userpic.html',
                              {'form': image_form},
                               context_instance=RequestContext(request))
