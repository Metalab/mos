<ul>{% for item in randomusers %}
    <li><a href="/wiki/Benutzer:{{ item.contactinfo.wiki_name }}" title="User page of {{ item.username }}"><img src="{{ item.contactinfo.image.url}}" /></a></li>
{% endfor %}</ul>
