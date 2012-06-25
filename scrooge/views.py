__version__ = "$Revision$"

from datetime import *

from dateutil.rrule import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from mos.members.models import *
from mos.scrooge.models import *
from django.contrib.auth import authenticate
from django.views.decorators.http import require_POST

import json

def json_response(obj):
    return HttpResponse(unicode(json.dumps(obj)), content_type='application/json')

#@login_required
@require_POST
def buy(request):
    if request.META['REMOTE_ADDR'] <> "127.0.0.1": raise Http404()
    #if not request.user.is_superuser: raise Http404('this resource does not exist (for your)')

    buy_request = json.loads(request.raw_post_data)
    button_id = buy_request["buttonId"]

    #get account and products, returning errors if not found
    try:
        account = Account.objects.get(credentialId=button_id)
    except Account.DoesNotExist:
        return json_response({'succeeded':False, 
            'errorMessage':'The account was not found. This incident will be reported!'})

    try:
        products = [Product.objects.get(ean=x) for x in buy_request['products']]
    except Product.DoesNotExist:
        return json_response({'succeeded':False, 
            'errorMessage':'One or more product was not found. Quit messing aroung!'})

    #compute booking data
    amount = reduce(lambda x,y: x+y, [p.price for p in products])
    description = 'bought %s' % ', '.join([x.name for x in products])
    
    booking = account.add_booking(-amount, description)
    if booking == None:
        return json_response({'succeeded':False, 
            'errorMessage':'You have insufficient funds, you are missing %s credits.' % float(amount-account.balance)})

    return json_response({'succeeded':True, 'totalPrice':float(amount), 'accountName':account.name})

def get_product_info(request, ean):
    try:
        product = Product.objects.get(ean=ean)
    except Product.DoesNotExist:
        raise Http404()

    return json_response({'name':unicode(product.name), 'ean':product.ean, 'price':float(product.price)})

def get_account_info(request, button_id):
    try:
        account = Account.objects.get(credentialId = button_id)
    except Account.DoesNotExist:
        raise Http404()

    return json_response({'accountName':unicode(account.name), 'balance':float(account.balance),
            'buttonId': button_id})

@require_POST
def load_credits(request):
    if request.META['REMOTE_ADDR'] <> "127.0.0.1": raise Http404()
    
    load_request = json.loads(request.raw_post_data)
    
    try:
        authorizer = Account.objects.get(credentialId=load_request["buttonIdAuthorization"])
        receiver = Account.objects.get(credentialId=load_request["buttonIdReceiver"])
    except Account.DoesNotExist:
        return json_response({'succeeded':False, 'errorMessage': 'account not found'})

    if authorizer.id == receiver.id:
        return json_response({'succeeded':False, 'errorMessage': 'you can not authorize yourself'})

    if authorizer.user == None:
        return json_response({'succeeded':False, 'errorMessage': 'authorizer is no member'})

    try:
        member = ContactInfo.objects.get(user=authorizer.user)
    except ContactInfo.DoesNotExist:
        return json_response({'succeeded':False, 'errorMessage': 'authorizer member info not found'})

    if not member.is_active_key_member():
        return json_response({'succeeded':False, 'errorMessage': 'authorizer is not an active key member'})

    transactionId='1234'
    amount = load_request["amount"]
    receiver.add_booking(amount, 'added credits, authorized by %s, transaction code %s' %(member.user.username, transactionId))
    
    return json_response({'transactionId':transactionId, 'accountNameAuthorization': member.user.username,
        'accountNameReceiver': receiver.name, 'succeeded':True})
