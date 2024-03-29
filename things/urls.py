from django.urls import path

from . import views

urlpatterns = [
    path('keys/<slug:thing>', views.thingusers_list),
    path('usage/<slug:thing>', views.thingusers_usage),
    path('stats/<slug:thing>', views.thing_usage_stats),
]
