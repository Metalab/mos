<h1>{{ HOS_NAME }} Members</h1>
<table width="100%" align="center" id="table_user_list">
{% for item in object_list %}
	<tr class="{% cycle even,odd %}">
		<td width="100px" style="text-align:center">
			{% if item.contactinfo_set.all.0.image %}
				<a href="../member/{{ item }}"><img class="thumb_with_text" src="{{ item.contactinfo_set.all.0.image.url }}"/></a>
			{% else %}
				<a href="../member/{{ item }}"><img src="/site_media/images/default_avatar.png"/></a>
			{% endif %}
		</td>
		<td>
			<b>{{ item }} <br></b>
			member since: {{ item.contactinfo_set.all.0.get_date_of_entry|date }} <br>
            {# debts: {{ item.contactinfo_set.all.0.get_debts }} Euro #}
		</td>
		<td>
			{% if item.contactinfo_set.all.0.get_wikilink %}
				<a href="{{ item.contactinfo_set.all.0.get_wikilink }}">wikiprofile</a><br>
			{% endif %}
			<a href="../member/{{ item }}">profile</a>
		</td>
	<tr>
{% endfor %}
<table>
