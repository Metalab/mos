{% if rendered_calendar %}
{{ rendered_calendar }}
<hr />
{% endif %}

{% with None as event %}
    {% load makeform %}
<div id="calendar-content">
    <ul class="eventlist">
    {% for event in latestevents %}
        {% makeform event cal.forms.EventForm event_form %}
        <li class="event">
        {% include "cal/new_eventinfo_nf.inc" with new=0 %}
        </li>
    {% endfor %}
    </ul>
{% endwith %}

<a href="{% url 'cal_index' %}">more...</a>
</div>
