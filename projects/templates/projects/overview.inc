<div id="projects-content">
		{% if errors %}
		  <div id="project-error-box" class="visible" style="border: 2px solid red; padding: 5px;">
			Following error(s) occured while editing <b>{{ e_project_name }}</b> : <br/>
			{{errors}}
			<a href="#" class="toggled btn-cancel" onclick="set_invisible($('project-error-box')); return false;">Ok</a></dd>
		  </div>
		{% endif %}
	<ul>

	{% for project in latestprojects %}
		<li>{% include "projects/projectinfo.inc" with new=0 %}</li>
	{% endfor %}
	</ul>
	{% include "projects/projectinfo.inc" with new=1%}
</div>

