<div id="project-content">
 <script>
   projectUpdateURL = "/project/";
 </script>
		{% if errors %}
		  <div id="project-error-box" class="visible" style="border: 2px solid red; padding: 5px;"> 
			Following error(s) occured while editing <b>{{ e_project_name }}</b> : <br/>
			{{errors}}
			<a href="#" class="toggled btn-cancel" onclick="set_invisible($('project-error-box')); return false;">Ok</a></dd>
		  </div>
		{% endif %}
	<ul>

	{% for project in latestprojects %}
		<li>{% include "projects/projectinfo.inc" %}</li>
	{% endfor %}
	</ul>
	{% with 1 as new %}
		{% include "projects/projectinfo.inc" %}
	{% endwith %}
</div>

