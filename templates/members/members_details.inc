{% ifequal error_type "permission" %}

{% endifequal %}

<div id="user_avatar">
	{% if item.contactinfo.image %}
		<img class="thumb_with_text" src="{{ item.contactinfo.image.url }}"/>
	{% else %}
		<img src="{{ STATIC_URL }}images/default_avatar.png"/>
	{% endif %}
	<a href="/member/{{user.username}}/update/userpic/" title="Change Userpic">Change Userpic</a>
</div>

<h3>Info</h3>
<table id="user_details">
	<tr>
		<td>Name:</td>
        <td>{{ item.first_name }} {{ item.last_name }} </td><td>{% if ea%}<a align="right" href='#'  onclick="set_visible($('member-edit-name')); return false;">Edit</a>{% endif %}</td>
    </tr>
    <tr>
         <td colspan="3">
            {% if ea %}
            <div class="edit {% ifequal error_type "name" %} visible {% else %} invisible {% endifequal %}" id='member-edit-name' style="border: 1px solid black; padding: 5px;">
                <form id='membmer-form-name' method="post" action="/member/{{user.username}}/update/name/" onsubmit="return false;" onKeyPress="
                if(enter_pressed(event)) {
                    myform = $('member-form-name');
                    new Ajax.Updater( $('container'), myform.readAttribute('action'), {
                      parameters: myform.serialize(true),
                    });
                }
                ">
		{% csrf_token %}
                    <dt><label>First Name</label> - <label>Last Name</label></dt>
		  {%  ifequal error_type "name" %}
		    <dd>{{ error_form.first_name.errors.0 }}  {{ error_form.first_name }} - {{ error_form.last_name.errors.0 }}  {{ error_form.last_name }}</dd>
		  {% else %}
		    <dd>
                        <input name='first_name' id="member-first_name" type="text" value='{{item.first_name}}'/>  - 
                        <input name='last_name' id="member-last_name" type="text" value='{{item.last_name}}'/>
                    </dd>
                  {% endifequal %}
                    <dt style="visibility: hidden">Submit:</dt>
                    <dd style="text-align: left">
                        <input type="button" value="Update" class="btn-update" onclick="
                        new Ajax.Updater( $('container'), $('membmer-form-name').readAttribute('action'), {
                          parameters: $('membmer-form-name').serialize(true),
                        });
                        "/>

                        <a href="#" class="toggled btn-cancel" onclick="set_invisible($('member-edit-name')); return false;">Cancel</a></dd>

                </form>
            </div>
            {% endif %}
        </td>
	</tr>


	<tr>
		<td>Member since:</td>
	        <td>{{ item.contactinfo.get_date_of_entry|date }}</td>

    	</tr>
{% if ea %}
   <tr><td colspan="3"><hr/></td></tr>
    <tr>
        <td colspan="3"><a href="/member/change_password/" title="Change Password">Change Password</a></th>
    </tr>
   <tr><td colspan="3"><hr/></td></tr>
{% endif %}

</table>

<h3>Contact info</h3>

<table id="user_contactinfo">
	<tr id='member-tr-email'>
		<td>Email:</td>
		<td>{{ item.email }}</td><td> {% if ea%}<a href='#'  onclick="set_visible($('member-edit-email')); return	false;">Edit</a>{% endif %}</td>
	</tr>
    <tr>
         <td colspan="3">
            {% if ea %}
            <div class="edit {% ifequal error_type "email" %} visible {% else %} invisible {% endifequal %}" id='member-edit-email' style="border: 1px solid black; padding: 5px; width:100%;">
                <form id='membmer-form-email' method="post" action="/member/{{user.username}}/update/email/" onsubmit="return false;" onKeyPress="
                if(enter_pressed(event)) {
                    myform = $('member-form-email');
                    new Ajax.Updater( $('container'), myform.readAttribute('action'), {
                      parameters: myform.serialize(true),
                    });
                }
                ">
		{% csrf_token %}
		  {% ifequal error_type "email" %}
		    <dt>New Email</dt>
		    <dd>{{ error_form.email.errors.0 }}   {{ error_form.email }} </dd>
		  {% else %}
                    <dt>New Email </dt>
                    <dd><input name='email' id="member-email" type="text" value='{{item.email}}' size="40"/></dd>
                  {% endifequal %}

                    <dt style="visibility: hidden">Submit:</dt>
                    <dd style="text-align: left">
                        <input type="button" value="Update" class="btn-update" onclick="
                        new Ajax.Updater( $('container'), $('membmer-form-email').readAttribute('action'), {
                          parameters: $('membmer-form-email').serialize(true),
                        });
                        "/>

                        <a href="#" class="toggled btn-cancel" onclick="set_invisible($('member-edit-email')); return false;">Cancel</a>

                </form>
            </div>
            {% endif %}
        </td>
    </tr>
	<tr>
		<td>Adress:</td>
		<td>{{ item.contactinfo.street }}; {{ item.contactinfo.postcode }} {{ item.contactinfo.city }}; {{ item.contactinfo.country }}</td><td> {% if ea%}<a href='#'  onclick="set_visible($('member-edit-adress')); return	false;">Edit</a>{% endif %}</td>
	</tr>

    <tr>
        <td colspan="3">
            {% if ea %}
            <div class="edit  {% ifequal error_type "adress" %} visible {% else %} invisible {% endifequal %}"  id='member-edit-adress' style="border: 1px solid black; padding: 5px; width:100%;">
                <form id='membmer-form-adress' method="post" action="/member/{{user.username}}/update/adress/" onsubmit="return false;" onKeyPress="
                if(enter_pressed(event)) {
                    myform = $('member-form-adress');
                    new Ajax.Updater( $('container'), myform.readAttribute('action'), {
                      parameters: myform.serialize(true),
                    });
                }
                ">
		{% csrf_token %}
                    <dt><label>Street</label> - <label>Postcode</label></dt>
		  {% ifequal error_type "adress" %}
		    <dd>{{ error_form.street.errors.0 }}  {{ error_form.street }} - {{ error_form.postcode.errors.0 }}  {{ error_form.postcode }}</dd>

                    <dt><label>City</label> - <label>Country</label></dt>

		    <dd>{{ error_form.city.errors.0 }}  {{ error_form.city }} - {{ error_form.country.errors.0 }}  {{ error_form.country }} </dd>

		  {% else %}

                    <dd>
                        <input name='street' id="member-street" type="text" value='{{ item.contactinfo.street }}'/>  - 
                        <input name='postcode' id="member-postcode" size="6" type="text" value=' {{ item.contactinfo.postcode }}'/>
                    </dd>
                    <dt><label>City</label> - <label>Country</label></dt>
                        <input name='city' id="member-city" type="text" value=' {{ item.contactinfo.city }}'/> - 
                        <input name='country' id="member-country" type="text" value=' {{ item.contactinfo.country }}'/>
                    </dd>
		  {% endifequal %}

                    <dt style="visibility: hidden">Submit:</dt>
                    <dd style="text-align: left">
                        <input type="button" value="Update" class="btn-update" onclick="
                        new Ajax.Updater( $('container'), $('membmer-form-adress').readAttribute('action'), {
                          parameters: $('membmer-form-adress').serialize(true),
                        });
                        "/>

                        <a href="#" class="toggled btn-cancel" onclick="set_invisible($('member-edit-adress')); return false;">Cancel</a>
                </form>
            </div>
            {% endif %}
        </td>
    </tr>

	<tr>
		<td>On intern list</td>
		{% if item.contactinfo.on_intern_list %}
			<td>yes ( {{ item.contactinfo.intern_list_email }} )</td>
		{% else %}
			<td>no</td>
		{% endif %}
                <td> {% if ea%}<a href='#'  onclick="set_visible($('member-edit-intern-list')); return false;">Edit</a>{% endif %}</td>

	</tr>
    <tr>
         <td colspan="3">
            {% if ea %}
            <div class="edit {% ifequal error_type "internlist" %} visible {% else %} invisible {% endifequal %}" id='member-edit-intern-list' style="border: 1px solid black; padding: 5px; width:100%;">
                <form id='membmer-form-internlist' method="post" action="/member/{{user.username}}/update/internlist/" onsubmit="return false;" onKeyPress="
                if(enter_pressed(event)) {
                    myform = $('member-form-internlist');
                    new Ajax.Updater( $('container'), myform.readAttribute('action'), {
                      parameters: myform.serialize(true),
                    });
                }
                ">
		{% csrf_token %}
                    <dt>On intern list </dt>
		  {% ifequal error_type "internlist" %}
		    <dd>{{ error_form.intern_list_email.errors.0 }}   {{ error_form.intern_list_email }} {{ error_form.on_intern_list }} </dd>
		  {% else %}
                    <dd><input name='on_intern_list' id="member-on_intern_list" type="checkbox" {% if item.contactinfo.on_intern_list%} checked="checked" {% endif %}  />
                        <input name='intern_list_email' id="member-intern_list_email" type="text" value="{{ item.contactinfo.intern_list_email }}" size="40"/>
                    </dd>
                  {% endifequal %}

                    <dt style="visibility: hidden">Submit:</dt>
                    <dd style="text-align: left">
                        <input type="button" value="Update" class="btn-update" onclick="
                        new Ajax.Updater( $('container'), $('membmer-form-internlist').readAttribute('action'), {
                          parameters: $('membmer-form-internlist').serialize(true),
                        });
                        "/>

                        <a href="#" class="toggled btn-cancel" onclick="set_invisible($('member-edit-internlist')); return false;">Cancel</a>

                </form>
            </div>
            {% endif %}
        </td>
    </tr>

    <tr>
		<td>Wiki name:</td>
		<td>{{ item.contactinfo.wiki_name }}</td>
	</tr>

    <tr>
		<td>Phone number:</td>
		<td>{{ item.contactinfo.phone_number }}</td>
	</tr>

    <tr>
		<td>Birthday:</td>
		<td>{{ item.contactinfo.birthday }}</td>
	</tr>
</table>


{# FIXME: don't list all the attributes manually #}

<h3>Bank data</h3>
<table id="user_bankdata">
    <tr>
		<td>Bank collection allowed:</td>
		<td>{{ item.paymentinfo.bank_collection_allowed|yesno }}</td>
	</tr>

    <tr>
		<td>Bank account owner:</td>
		<td>{{ item.paymentinfo.bank_account_owner }}</td>
	</tr>

    <tr>
		<td>Bank account number:</td>
		<td>{{ item.paymentinfo.bank_account_number }}</td>
	</tr>

	<tr>
		<td>Bank name:</td>
		<td>{{ item.paymentinfo.bank_name }}</td>
	</tr>

	<tr>
		<td>Bank code:</td>
		<td>{{ item.paymentinfo.bank_code }}</td>
	</tr>

	<tr>
		<td>Bank IBAN:</td>
		<td>{{ item.paymentinfo.bank_account_iban }}</td>
	</tr>

	<tr>
		<td>Bank BIC:</td>
		<td>{{ item.paymentinfo.bank_account_bic }}</td>
	</tr>

	<tr>
		<td>Bank mandate reference:</td>
		<td>{{ item.paymentinfo.bank_account_mandate_reference }}</td>
	</tr>

    <tr>
        <td>Date of sigining:</td>
        <td>{{ item.paymentinfo.bank_account_date_of_signing }}</td>
    </tr>

	<tr>
		<td>Mode:</td>
		<td>{{ item.paymentinfo.bank_collection_mode }}</td>
	</tr>

</table>


<h3>Payments</h3>
<table id="user_paymenthistory">

	{% for p in item.payment_set.all %}
		<tr>
			<td>{{ p.amount }} Euro</td>
			<td>paid on {{ p.date|date:"d.m.Y" }} ({{ p.comment }} {{ p.method }})</td>
		</tr>
	{% endfor %}
</table>


<h3>Membership periods</h3>
<table id="user_memberhistory">
	{% for mp in item.membershipperiod_set.all %}
		<tr>
			<td>{{ mp.begin|date:"d.m.Y" }} - {% if mp.end %}{{ mp.end|date:"d.m.Y" }}{% else %}now{% endif %}</td>
			<td>{{ mp.get_duration_in_month }} month as {{ mp.kind_of_membership }}</td>
		</tr>
	{% endfor %}
</table>
