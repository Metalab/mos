<h1>{{ HOS_NAME }} Members</h1>
<table width="100%" align="center" id="table_user_list" class="sortable">
<tr>

<th class="sorttable_nosort"></th>
<th>name</th>
<th>member since</th>
<th class="sorttable_nosort"></th>
<th class="sorttable_numeric">debts</th>

</tr>
{% for item in object_list %}
	<tr class="{% cycle even,odd %}">
		<td width="100px" style="text-align:center">
			{% if item.contactinfo.image %}
				<a href="../member/{{ item }}"><img class="thumb_with_text" src="{{ item.contactinfo.image.url }}"/></a>
			{% else %}
				<a href="../member/{{ item }}"><img src="{{ STATIC_URL }}images/default_avatar.png"/></a>
			{% endif %}
        </td>
        <td>
			<b>{{ item }} <br></b>
        </td>
        <td>
			{{ item.contactinfo.get_date_of_entry|date }} <br>
		</td>
		<td>
			{% if item.contactinfo.get_wikilink %}
				<a href="{{ item.contactinfo.get_wikilink }}">wikiprofile</a><br>
			{% endif %}
			<a href="../member/{{ item }}">profile</a>
			{{item.first_name}} {{item.last_name}} <br />
        </td>
        <td>
			{{ item.contactinfo.get_debts|floatformat:2 }} Euro
		</td>
	<tr>
{% endfor %}
<table>
