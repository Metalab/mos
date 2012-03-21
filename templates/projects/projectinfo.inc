<div id='projectcontainer{{project.id}}'>
	<p class="project visible {% cycle odd,even %}" id="project-view-{{project.id}}">
		{% if project.wikiPage %}<a href="/wiki/{{ project.wikiPage }}"> {% endif %}{{ project.name }}{% if project.wikiPage %}</a>{% endif %}
		{% if user.is_authenticated %}<a href='#' class="{%if not new %}hoverHidden{%endif%}" onclick="toggleView('project','{{project.id}}', 1); return false;">{%if not new %}Edit{%else%}Create New Project{%endif%}</a>{% endif %}{% if project.teaser %}<br/><small>{{ project.teaser }}</small>{%endif%}
	</p>
	{% if user.is_authenticated %}
	<div class="edit invisible" id='project-edit-{{project.id}}'>
		<form id='project-form-{{project.id}}' method="post" action="/project/{% if new %}new{%else%}{{project.id}}/update{%endif%}/" onsubmit="return false;" onKeyPress="
		if(enter_pressed(event)) { submit_form($('project-form-{{project.id}}'), $('projects-content')); }"> 

			<dl>
			<dt><label>Name (*):</label></dt>
			<dd><input name='name' id="project-name-{{project.id}}" type="text" value='{{ project.name }}'/></dd>
			
			<dt><label>Teaser:</label></dt>
			<dd><input name='teaser' id="project-teaser-{{project.id}}" type="text" value='{{ project.teaser }}'/></dd>
		
			<dt><label>Wiki Page</label></dt>
			<dd><input name='wikiPage' id="project-wikiPage-{{project.id}}" type="text" value='{{ project.wikiPage }}'/></dd>
		
			<dt><label>Finished:</label></dt>
            <dd><input name='finished_at' class='vDateField' id="project-finishedDate-{{project.id}}" type='text' value='{% if project.finished_at %}{{ project.finished_at }}{% endif %}' /></dd>
			<dt>* -> required field</dt>
			<dt style="visibility: hidden">Submit:</dt>
			<dd style="text-align: right">
			{% if not new %}
				<input type="button" value="Update" class="btn-update" onclick=" submit_form('project', '{{project.id}}');">
				<input type="button" value="Delete" class="btn-delete" onclick="delete_entry('project', '{{project.id}}');">
			{% else %}
				<input type="button" class="btn-create" value="Create" onclick=" submit_form('project', '{{project.id}}');">
				
			{% endif %}

				<a href="#" class="toggled btn-cancel" onclick="toggleView('project', '{{project.id}}', 0); return false;">Cancel</a>
			</dd>		
			</dl>
		</form>
	</div>
	{% endif %}
</div>
