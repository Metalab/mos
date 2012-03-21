<div id='projectcontainer{{project_form.instance.id|default_if_none:""}}'>

	<p class="project {% ifequal project_error_id project_form.instance.id %}invisible{% endifequal%}" id="project-view-{{project_form.instance.id|default_if_none:""}}">
		{% if project.wikiPage %}<a href="/wiki/{{ project.wikiPage }}"> {% endif %}{{ project.name }}{% if project.wikiPage %}</a>{% endif %}
		{% if user.is_authenticated %}<a href='#' class="{%if not new %}hoverHidden{%endif%}" onclick="toggleView('project','{% if not new %}{{project_form.instance.id|default_if_none:""}}{% endif %}', 1); return false;">{%if not new %}Edit{%else%}Create New Project{%endif%}</a>{% endif %}{% if project.teaser %}<br/><small>{{ project.teaser }}</small>{%endif%}
	</p>
	{% if user.is_authenticated %}
	<div class="edit {% ifnotequal project_error_id project_form.instance.id %}invisible{% endifnotequal%}" id="project-edit-{{project_form.instance.id|default_if_none:""}}">
		<form id="project-form-{{project_form.instance.id|default_if_none:""}}" method="post" action="/project/{% if new %}new{%else%}{{project.id}}/update{%endif%}/" onsubmit="return false;" onKeyPress="
		if(enter_pressed(event)) { submit_form($('project-form-{{project_form.instance.id|default_if_none:""}}'), $('projects-content')); }"> 

			<dl>
			<dt><label>Name (*):</label></dt>
			{% if project_form.name.errors %}
			   <dt>{{ project_form.name.errors }}</dt>
			{% endif %}
			<dd>{{ project_form.name }}</dd>
			
			<dt><label>Teaser:</label></dt>
			<dd>{{project_form.teaser}}</dd>
		
			<dt><label>Wiki Page</label></dt>
			<dd>{{project_form.wikiPage}}</dd>
		
			<dt><label>Finished:</label></dt>
            <dd>{{project_form.finished_at}}</dd>
			<dt>* -> required field</dt>
			<dt style="visibility: hidden">Submit:</dt>
			<dd style="text-align: right">
			{% if not new %}
				<input type="button" value="Update" class="btn-update" onclick="submit_form('project', '{{project_form.instance.id|default_if_none:""}}');">
				<input type="button" value="Delete" class="btn-delete" onclick="delete_entry('project', '{{project_form.instance.id|default_if_none:""}}');/">
			{% else %}
				<input type="button" class="btn-create" value="Create" onclick="submit_form('project', '{{project_form.instance.id|default_if_none:""}}');">
				
			{% endif %}

				<a href="#" class="toggled btn-cancel" onclick="toggleView('project', '{% if not new %}{{project_form.instance.id|default_if_none:""}}{% endif %}', 0); return false;">Cancel</a>
			</dd>		
			</dl>
		</form>
	</div>
	{% endif %}
</div>
