{{ rendered_calendar }}
{% if rendered_calendar %}<hr />{% endif %}

{% with None as event %}
    {% load makeform %}
<div id="calendar-content">
     <script>
       var came_from = '{{came_from}}';
     </script>
    <ul>
	{% for event in latestevents %}
        {% makeform event mos.cal.forms.EventForm event_form %}
		<li>{% include "cal/eventinfo_nf.inc" %}</li>
	{% endfor %}
    </ul>

	{% with 1 as new %}
        {% makeform None mos.cal.forms.EventForm event_form %}
        {% include "cal/eventinfo_nf.inc" %}
        {% endwith %}
	{% endwith %}
	{% if not all_events %} <p  id="calender_morelink" style="text-align: right"><a href="/calendar/{% if location %}special/Location/{{location.name}}{% else %}{% if category %}special/Category/{{category.name}}{% endif %}{% endif %}">more...</a></p> {% endif %}
</div>
