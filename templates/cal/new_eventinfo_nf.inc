<p class="{% if event.past %}past_event{% else %}event{% endif %}" id="calendar-view-{{event.id}}">
{% if not new %}
<a class="event_ical" href="{% if not new %}{{event.get_icalendar_url}}{% else %}{% url "cal.views.complete_ical" %}{%endif %}">ical
</a>
<span class="event_date">
{{ event.startDate|date:"D d.m.Y H:i" }} {% if event.endDate %} - {% if event.start_end_date_eq %} {{ event.endDate|date:"H:i" }} {% else %} {{ event.endDate|date:"D d.m.Y H:i" }} {% endif %} {% endif %}
    </span>
    {% if event.location%}
    <span class="location"> @
    <a href="/calendar/special/Location/{{ event.location }}/">
    {{ event.location }}
    </a>
    </span>
    {% endif %}

<h4 class="event_title">
  {% if event.wikiPage %}
    <a href="/wiki/{{event.wikiPage}}">{{ event.name }}</a>
  {% else %}
    {{ event.name }}
  {% endif %}
</h4>

{% if event.teaser %}
  <span class="teaser">{{ event.teaser }}</span>
{% endif %}

{% if event.category %}
  <span class="category">
    <a href="/calendar/special/Category/{{ event.category }}/">
      {{ event.category }}
    </a>
  </span>
{% endif %}

{% endif %}
{% if user.is_authenticated and not edit_disabled %}
<a href='#' class="{%if not new %}hoverHidden{%endif%}" onclick="toggleView('calendar', '{% if not new %}{{event.id|default_if_none:""}}{% endif %}', 1); return false;">{%if not new %}Edit{%else%}Create New Event{%endif%}</a> {% endif %}

{% if user.is_authenticated %}

<div class="{% if not event_has_error %}invisible {%endif%}edit" id='calendar-edit-{% if not new %}{{event.id|default_if_none:""}}{% endif %}'>
<form
  id='calendar-form-{{event.id|default_if_none:""}}'
  method="post"
  action="/calendar/{% if new %}new{%else%}{{event.id|default_if_none:""}}/update{%endif%}/"
  onsubmit="return false;"
  onKeyPress="if(enter_pressed(event)){ submit_form($('calendar-form-{{event.id|default_if_none:""}}'), $('eventcontainer{{event.id|default_if_none:""}}')); }">
   {% csrf_token %}
  <dl>
    <dt><label><b>Event Name</b>:* - Teaser:</label></dt>
    <dd>
      {{ event_form.name }} - <br/>
      {{ event_form.teaser }}
    </dd>

    {% if event_form.name.errors %}
      <dd> {{ event_form.name.errors }}</dd>
    {% endif %}

    <dt>
      <label><b>Wiki Page</b>:*</label>
    </dt>
    <dd>{{ event_form.wikiPage }}</dd>

    {% if event_form.wikiPage.errors %}
      <dd>{{ event_form.wikiPage.errors }}</dd>
    {% endif %}

    <dt><label><b>Start</b>:*</label></dt>
    <dd> {{ event_form.startDate }} </dd>

    {% if event_form.startDate.errors %}
    <dd> {{ event_form.startDate.errors }} </dd>
    {% endif %}

    <dt><label>End:</label></dt>

    <dd> {{ event_form.endDate }}</dd>
      {% if event_form.endDate.errors %}
    <dd> {{ event_form.endDate.errors }} </dd>
    {% endif %}

    <dt><label>Location:</label></dt>
      <dd> {{ event_form.location }}</dd>
      {% if event_form.location.errors %}
        <dd> {{ event_form.location.errors }} </dd>
      {% endif %}

    <dt><label>Category:</label></dt>
    <dd> {{ event_form.category }}</dd>

    {% if event_form.category.errors %}
      <dd> {{ event_errors.category }} </dd>
    {% endif %}

    <legend> (*) -> required field </legend>

    <dt style="visibility: hidden">Submit:</dt>
    <dd style="text-align: right;">

    {% if not new %}
      <input type="button" value="Update" onclick="submit_event('{{event.id|default_if_none:""}}');">
      <input type="button" value="Delete" onclick="delete_event('{{event.id|default_if_none:""}}');">
    {% else %}
      <input type="button" value="Create" onclick="submit_event('{{event.id|default_if_none:""}}');">
    {% endif %}

    <a href="#"
      class="toggled"
      onclick="toggleView('calendar', '{% if not new %}{{event.id|default_if_none:""}}{% endif %}', 0); return false;">Cancel</a>
    </dd>
  </dl>
  <a 
    style="padding:0.5em; border:1px solid red; background:#ffbbbb;"
    href="http://metalab.at/wiki/Kalender">
    Terminkonflikt?
  </a>
	</form>
	</div>
	{% endif %}
