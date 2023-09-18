
<div id="calendarcontainer{{event.id|default_if_none:""}}">


  {% if not new %}
  <p class="event {% if event.past %}past_event{% else %}event{% endif %}" id="calendar-view-{{event.id|default_if_none:""}}">
    <span class="event_date">{{ event.startDate|date:"D d.m.Y H:i" }} {% if event.endDate %} - {% if event.start_end_date_eq %} {{ event.endDate|date:"H:i" }} {% else %} {{ event.endDate|date:"D d.m.Y H:i" }} {% endif %} {% endif %}</span>
		{% if event.wikiPage %}<a href="/wiki/{{event.wikiPage}}"> {% endif %}<span class="name">{{ event.name }}</span>{% if event.wikiPage %}</a>{% endif %}
		{% if event.teaser %}<span class="teaser">{{ event.teaser }}</span>{% endif %}
		{% if event.category %}<span class="category"> | <a href="/calendar/special/Category/{{ event.category }}/">{{ event.category }}</a></span>{% endif %}
		{% if event.location%}<span class="location"> | <a href="/calendar/special/Location/{{ event.location }}/">{{ event.location }}</a></span>{% endif %}

    {% if user.is_authenticated and not edit_disabled %}
      <a href='#' class="hoverHidden" onclick="toggleView('calendar', '{{event.id}}', 1); return false;">
        Edit
      </a>
    {%endif %}
      <a class="hoverHidden" href="{{event.get_icalendar_url}}">📅 ical</a>
    {% if user.is_authenticated %}
      <span class="hoverHidden">| created by</span> <a class="hoverHidden" href="/wiki/Benutzer:{{ event.created_by }}">{{ event.created_by }}</a>
    {%endif %}
  </p>

  {%else%}
    <p><a href="{% url 'small_ical' %}">Download current events in ical format</a></p>
    {% if user.is_authenticated and not edit_disabled %}
    <p>
      <a href='#' class="btn" onclick="toggleView('calendar', '', 1); return false;">
        Create new event
      </a>
    </p>
    {%endif %}
  {%endif %}


	{% if user.is_authenticated %}
		{% include "cal/event_form.inc" with from_nf=1 %}
	{% endif %}
</div>
