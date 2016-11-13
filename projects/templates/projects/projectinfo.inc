{% with form_id=project.id|default_if_none:'' %}
<div id='projectcontainer{{ form_id }}'>
	<p class="project{% if project_form.errors %} invisible{% endif %}" id="project-view-{{ form_id }}">
		{% if project.wikiPage %}<a href="/wiki/{{ project.wikiPage }}"> {% endif %}{{ project.name }}{% if project.wikiPage %}</a>{% endif %}
		{% if user.is_authenticated %}<a href='#' class="{%if not new %}hoverHidden{%endif%}" onclick="toggleView('project', '{{ form_id }}', 1); return false;">{%if not new %}Edit{%else%}Create New Project{%endif%}</a>{% endif %}{% if project.teaser %}<br/><small>{{ project.teaser }}</small>{%endif%}
	</p>
	{% if user.is_authenticated %}
    <div class="edit{% if not project_form.errors %} invisible{% endif %}" id="project-edit-{{ form_id }}">
		<form id="project-form-{{ form_id }}" method="post" action="/project/{% if new %}new{% else %}{{ form_id }}/update{% endif %}/" onsubmit="return false;" onKeyPress="
		if (enter_pressed(event)) { submit_form('project', '{{ form_id }}'); }">
            {% csrf_token %}
			<dl>
			<dt><label>Name (*):</label></dt>
			{% if project_form.name.errors %}<dt>{{ project_form.name.errors }}</dt>{% endif %}
			<dd><input name='name' id="project-name-{{ form_id }}" type="text" value='{{ project.name }}'/></dd>

			<dt><label>Teaser:</label></dt>
			<dd><input name='teaser' id="project-teaser-{{ form_id }}" type="text" value='{{ project.teaser }}'/></dd>

			<dt><label>Wiki Page</label></dt>
			<dd><input name='wikiPage' id="project-wikiPage-{{ form_id }}" type="text" value='{{ project.wikiPage }}'/></dd>

			<dt><label>Finished:</label></dt>
            <dd><input name='finished_at' class='vDateField' id="project-finishedDate-{{ form_id }}" type='text' value='{% if project.finished_at %}{{ project.finished_at|date:"Y-m-d" }}{% endif %}' /></dd>
			<dt>* -> required field</dt>
			<dt style="visibility: hidden">Submit:</dt>
			<dd style="text-align: right">
			{% if not new %}
				<input type="button" value="Update" class="btn-update" onclick="submit_form('project', '{{ form_id }}');">
				<input type="button" value="Delete" class="btn-delete" onclick="delete_entry('project', '{{ form_id }}');">
			{% else %}
				<input type="button" class="btn-create" value="Create" onclick="submit_form('project', '');">
			{% endif %}
            <a href="#" class="toggled btn-cancel" onclick="toggleView('project', '{{ form_id }}', 0); return false;">Cancel</a>
			</dd>
			</dl>
		</form>
	</div>
	{% endif %}
</div>
{% endwith %}
