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

        <dt><label><b>Wiki Image Page</b>:</label></dt>
        <dd>  {{ event_form.wikiImagePage }} </dd>
        {% if event_form.wikiImagePage.errors %}
            <dd> {{ event_form.wikiImagePage.errors }} </dd>
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
        <dd class="form-buttons">
            <div class="status-indicator"></div>
            {% if not new %}
                <input type="button" value="Update" onclick="submit_event('{{event.id|default_if_none:""}}');">
                {% if from_nf %}
                    <input type="button" value="Delete" onclick="delete_event('{{event.id|default_if_none:""}}');">
                {% endif %}
            {% else %}
                <input type="button" value="Create" onclick="submit_event('{{event.id|default_if_none:""}}');">
            {% endif %}
            {% if from_nf %}
                <a href="#" class="toggled" onclick="toggleView('calendar', '{% if not new %}{{event.id|default_if_none:""}}{% endif %}', 0); return false;">Cancel</a>
            {% endif %}
        </dd>
        </dl>
    </form>
</div>
