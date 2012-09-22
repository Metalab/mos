
<tr class="{% if event.past %}past_event{% else %}event{% endif %}">
    <td style="text-align: right;">
        {{ event.format_duration }}
    </td>
    <td>
        {% if event.wikiPage %}
            <a href="/wiki/{{event.wikiPage}}">{{ event.name }}</a>
        {% else %}
            {{ event.name }}
        {% endif %}

        {% if user.is_authenticated and not edit_disabled %}
            <span class="detail_link">(<a href="{{event.get_edit_url}}">edit</a>)</span>
        {% endif %}

        <span class="detail_link">(<a href="{{event.get_icalendar_url}}">ics</a>)</span>

        {% if event.teaser or event.location %}
            <small><br>

            {% if event.teaser %}
                {{ event.teaser }}
            {% endif %}

            {% if event.teaser and event.location %}
                |
            {% endif %}

            {% if event.location %}
                <a href="/calendar/special/Location/{{ event.location }}/">{{ event.location }}</a>
            {% endif %}

            </small>
        {% endif %}
        <!-- XXX: Re-add category: event.category -->
    </td>
</tr>

<!-- XXX: Refactor this to a separate edit event page

	{% if user.is_authenticated %}

    <div class="{% if not event_has_error %}invisible {%endif%}edit" id='calendar-edit-{% if not new %}{{event.id|default_if_none:""}}{% endif %}'>
		<form id='calendar-form-{{event.id|default_if_none:""}}' method="post" action="/calendar/{% if new %}new{%else%}{{event.id|default_if_none:""}}/update{%endif%}/" onsubmit="return false;" onKeyPress="if(enter_pressed(event)){ submit_form($('calendar-form-{{event.id|default_if_none:""}}'), $('eventcontainer{{event.id|default_if_none:""}}')); }">
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

			<a href="#" class="toggled" onclick="toggleView('calendar', '{% if not new %}{{event.id|default_if_none:""}}{% endif %}', 0); return false;">Cancel</a>
            </dd>
            </dl>
            <a style="padding:0.5em; border:1px solid red; background:#ffbbbb;" href="http://metalab.at/wiki/Kalender">Terminkonflikt?</a>
		</form>
	</div>
	{% endif %}

-->

</div>
