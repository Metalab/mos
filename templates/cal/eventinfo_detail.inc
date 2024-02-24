<div class="eventinfo-detail">

  <div id="calendarcontainer{{event.id|default_if_none:""}}">

    <div class="event {% if event.past %}past_event{% else %}event{% endif %}" id="calendar-view-{{event.id|default_if_none:""}}">

      {% if event.past %}
      <div class="notification warning">Achtung: Event liegt bereits in der Vergangenheit!</div>
      {% endif %}

      <h1 id="site-name">Event: <span class="name">{{ event.name }}</span></h1>
      <p>
        {% if event.teaser %}<span class="teaser">Teaser: {{ event.teaser }}</span>{% endif %}
      </p>
      {% if event.category %}
      <p>
        <span class="category">Kategorie: <a href="/calendar/special/Category/{{ event.category }}/">{{ event.category }}</a></span>
      </p>
      {% endif %}
      <p>
        <span class="event_date">
          {{ event.startDate|date:"D d.m.Y H:i" }} {% if event.endDate %} - {% if event.start_end_date_eq %} {{ event.endDate|date:"H:i" }} {% else %} {{ event.endDate|date:"D d.m.Y H:i" }} {% endif %} {% endif %}
        </span>
      </p>
      {% if event.location%}
      <p>
        <span class="location">Ort: <a href="/calendar/special/Location/{{ event.location }}/">{{ event.location }}</a></span>
      </p>
      {% endif %}
      {% if event.wikiPage %}
      <p>
        Details: <a href="/wiki/{{event.wikiPage}}"> {{ request.get_host }}/wiki/{{event.wikiPage}}</a>
      </p>
      {% endif %}

      {% if user.is_authenticated %}
      <p>
        {% if event.advertise %}
          Dieser Event kann öffentlich beworben werden.
        {% else %}
          Dieser Event soll nicht öffentlich beworben werden.
        {% endif %}
      </p>
      <p>
        ical: <a href="{{event.get_icalendar_url}}">{{ request.get_host }}{{event.get_icalendar_url}}</a>
      </p>
      <p>
        Das Event wurde am {{ event.created_at|date:"d.m.Y" }} um {{ event.created_at|date:"H:i" }} von <i><a href="/wiki/Benutzer:{{ event.created_by }}">{{ event.created_by }}</a></i> erstellt.</a>
      </p>

      {% if not edit_disabled %}
      <p>
        <a class="btn" href='#' onclick="toggleView('calendar', '{{event.id}}', 1); return false;">
          Edit
        </a>

        <a class="btn" href='#' type="button" onclick="delete_event('{{event.id|default_if_none:""}}');">
          Delete
        </a>

      </p>
      {% endif %}

      {% endif %}

    </div>

  	{% if user.is_authenticated %}
      {% include "cal/event_form.inc" with from_nf=0 %}
  	{% endif %}
  </div>
</div>
