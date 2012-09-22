{{ rendered_calendar }}
{% if rendered_calendar %}<hr />{% endif %}

<div id="calendar-content">
{% with None as event %}
    {% load makeform %}

    <table>
        {% for event in latestevents %}
            {% ifchanged %}
                <tr><th>{{ event.start_day }}</th><td>&nbsp;</td></tr>
            {% endifchanged %}
            {% include "cal/eventinfo_nf.inc" %}
        {% endfor %}
    </table>

    <h2>FIXME: Add event form here</h3>
{% endwith %}

{% if not all_events %}
    <p id="calender_morelink" style="text-align: right;">
        <a href="/calendar/{% if location %}special/Location/{{location.name}}{% else %}{% if category %}special/Category/{{category.name}}{% endif %}{% endif %}">more...</a>
    </p>
{% endif %}
</div>
