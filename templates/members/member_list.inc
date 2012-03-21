<h2>Public Users</h2>
<ul class="user-list-pictures">{% for item in object_list %}{% if item.contactinfo_set.all.0.image %}
    <li class="image-col-{% cycle one,two,three,four %}">
    <p class="user-list-name">{% if item.contactinfo_set.all.0.get_wikilink %}<a href="{{ item.contactinfo_set.all.0.get_wikilink }}" title="Userpage of {{item.username}}">{% endif %}{{ item.username }}{% if item.contactinfo_set.all.0.get_wikilink %}</a>{% endif %}</p>
        <p style="width: 210px;"><img src="{{ item.contactinfo_set.all.0.image.url }}" alt="Picture of {{ item.username }}" title="Picture of {{ item.username }}" style="max-width: 200px;" /></p>
    </li>
{% endif %}{% endfor %}</ul>

{% if user.is_authenticated %}
<h2>Users without Picture</h2>
<ul>{% for item in object_list %}{% if not item.contactinfo_set.all.0.image %}
    <li>{{ item.username }}</li>
{% endif %}{% endfor %}</ul>{% endif %}

