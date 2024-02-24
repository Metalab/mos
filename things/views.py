from members.models import get_active_and_future_members
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from .models import Thing
from .models import ThingUser
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def thingusers_list(request, thing):
    try:
        thing = Thing.objects.get(slug=thing)
        supplied_token = request.META["HTTP_X_TOKEN"]
    except LookupError:
        return HttpResponseBadRequest(
            "curl https://metalab.at/things/keys/THING -H 'X-TOKEN: get_this_from_vorstand'",
        )
    except Thing.DoesNotExist:
        return HttpResponseNotFound()

    if thing.token != supplied_token:
        return HttpResponseForbidden("token invalid")

    members_with_thing = get_active_and_future_members().filter(thingusers__thing=thing)

    text = '\n'.join(
        (m.contactinfo.key_id or "") + "," + m.username
        for m in members_with_thing
    )
    return HttpResponse(text, content_type='text/plain')
