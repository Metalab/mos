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

      <div class="{% if not event_has_error %}invisible {%endif%}edit-form" id='calendar-edit-{% if not new %}{{event.id|default_if_none:""}}{% endif %}'>
  		<form id='calendar-form-{{event.id|default_if_none:""}}' method="post" action="/calendar/{% if new %}new{%else%}{{event.id|default_if_none:""}}/update{%endif%}/" onsubmit="return false;" onKeyPress="if(enter_pressed(event)){ submit_form($('calendar-form-{{event.id|default_if_none:""}}'), $('eventcontainer{{event.id|default_if_none:""}}')); }">
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

  			<dt><label><b>Wiki Page</b>:*</label></dt>
  			<dd>  {{ event_form.wikiPage }} </dd>
  			{% if event_form.wikiPage.errors %}
  			   <dd> {{ event_form.wikiPage.errors }} </dd>
  			{% endif %}

  			<dt><label><b>Start</b>:*</label></dt>
  			<dd> {{ event_form.startDate }} </dd>
  			{% if event_form.startDate.errors %}
  			   <dd> {{ event_form.startDate.errors }} </dd>
  			{% endif %}

  			<dt><label><b>End</b>:</label></dt>

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

              <dt><label>This event can be advertised to potential newcomers:</label></dt>
              <dd> {{ event_form.advertise }}</dd>
              {% if event_form.advertise.errors %}
                  <dd> {{ event_errors.advertise }} </dd>
              {% endif %}

              <legend> (*) -> required field </legend>


              <dt style="visibility: hidden">Submit:</dt>
              <dd>
  			{% if not new %}

  				<input type="button" class="btn" value="Update" onclick="submit_event('{{event.id|default_if_none:""}}');">

              {% else %}
  				<input type="button" class="btn" value="Create" onclick="submit_event('{{event.id|default_if_none:""}}');">
              {% endif %}
              </dd>
              </dl>
        <a style="padding:0.5em; border:1px solid red; background:#ffbbbb; display:inline-block; margin: .5em 0;" href="http://metalab.at/wiki/Kalender">Terminkonflikt?</a>
  		</form>
  	</div>
  	{% endif %}
  </div>

  <div id="calendar-update"></div>
</div>
