<h1><a href="http://metalab.at/wiki/Spezial:Letzte_Änderungen">Letzte Änderungen</a></h1>
{% for change in latestchanges %}
    <a href="{{ change.link }}">{{ change.title }}</a><br/><small>- {{ change.author }}</small><br/>
{% endfor %}