{% if herelist %}
    <h3>Derzeit im Metalab</h3>
    <ul>
    {% for item in herelist %}
       <li>{{ item.nick }}</li> 
    {% endfor %}
    </ul>
{% endif %}
