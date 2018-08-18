{% if rendered_calendar %}
{{ rendered_calendar }}
<hr />
{% endif %}

{% with None as event %}
    {% load makeform %}
<div id="calendar-content">

    <script>
    var came_from = '{{came_from}}';
    </script>

    <ul class="eventlist">
    {% for event in latestevents %}
        {% makeform event cal.forms.EventForm event_form %}
        <li class="event">
        {% include "cal/new_eventinfo_nf.inc" with new=0 %}
        </li>
    {% endfor %}
    </ul>
{% endwith %}

<a href="{{ more_events_url }}">more...</a>
</div>
