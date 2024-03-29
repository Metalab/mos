<h1>Metalab Mitglieder</h1>
<table width="100%" align="center" id="table_user_list">
{% for item in object_list %}
	<tr class="{% cycle "even" "odd" %}">
		<td width="100px" style="text-align:center">
			{% if item.contactinfo.image %}
				<a href="../member/{{ item }}"><img class="thumb_with_text" src="{{ item.contactinfo.image.url }}"/></a>
			{% else %}
				<a href="../member/{{ item }}"><img src="{{ STATIC_URL }}images/default_avatar.png"/></a>
			{% endif %}
		</td>
		<td>
			<b>{{ item }} <br></b>
			member since: {{ item.contactinfo.get_date_of_first_join|date }} <br>
            {# debts: {{ item.contactinfo.get_debts }} Euro #}
		</td>
		<td>
			<a href="../admin/auth/user/{{ item.id }}">edit</a> <br>
			{% if item.contactinfo.get_wikilink %}
				<a href="{{ item.contactinfo.get_wikilink }}">wikiprofile</a><br>
			{% endif %}
			<a href="../member/{{ item }}">profile</a>
		</td>
	<tr>
{% endfor %}
<table>
