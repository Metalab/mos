from django.urls import path

import announce.views

urlpatterns = [
    path('', announce.views.announce),
]
