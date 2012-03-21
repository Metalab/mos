<h1><a href="{{ HOS_WIKI_CHANGE_URL }}">Letzte Änderungen</a></h1>
{% for change in latestchanges %}
    <a href="{{ change.link }}">{{ change.title }}</a><br/><small>- {{ change.author }}</small><br/>
{% endfor %}
