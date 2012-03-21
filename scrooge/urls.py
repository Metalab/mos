from django.conf.urls.defaults import *

from mos.scrooge.models import *


urlpatterns = patterns('',
    (r'^json/buy$', 'mos.scrooge.views.buy'),
    (r'^json/insert_coin$', 'mos.scrooge.views.load_credits'),
    (r'^json/account/(?P<button_id>(\w|-)+)$', 'mos.scrooge.views.get_account_info'),
    (r'^json/(?P<ean>\w+)$', 'mos.scrooge.views.get_product_info'),
)
