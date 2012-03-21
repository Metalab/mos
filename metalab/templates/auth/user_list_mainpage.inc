<ul>{% for item in randomusers %}
    <li><a href="/wiki/Benutzer:{{ item.contactinfo_set.all.0.wiki_name }}" title="User page of {{ item.username }}"><img src="{{ item.contactinfo_set.all.0.get_image_url}}" /></a></li>
{% endfor %}</ul>
