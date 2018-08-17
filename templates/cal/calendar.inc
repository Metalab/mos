{{ rendered_calendar }}
{% if rendered_calendar %}<hr />{% endif %}

{% with None as event %}
    {% load makeform %}
<div id="calendar-content">
     <script>
       var came_from = '{{came_from}}';
     </script>
    <ul class="eventlist">
	{% for event in latestevents %}
        {% makeform event cal.forms.EventForm event_form %}
		<li class="event">{% include "cal/eventinfo_nf.inc" with new=0 %}</li>
	{% endfor %}
    </ul>

        {% makeform None cal.forms.EventForm event_form %}
        {% include "cal/eventinfo_nf.inc" with new=1 %}
	{% endwith %}
	{% if not all_events %} <p  id="calender_morelink" style="text-align: right"><a href="/calendar/{% if location %}special/Location/{{location.name}}{% else %}{% if category %}special/Category/{{category.name}}{% endif %}{% endif %}">more...</a></p> {% endif %}
</div>
