function addEvent(obj, evType, fn, useCapture){
  if (obj.addEventListener){
    obj.addEventListener(evType, fn, useCapture);
    return true;
  } else if (obj.attachEvent){
    var r = obj.attachEvent("on"+evType, fn);
    return r;
  } else {
    alert("Handler could not be attached");
  }
}

function gettext(lol) {
	return lol;
}

function submit_form(type, id){
    myform = $(type + '-form-' + id);
    new Ajax.Updater($(type + 'container' + id), myform.readAttribute('action'), {
                  parameters: myform.serialize(true),
    });
 
}

function delete_event(id) {
    var frm = $('calendar-form-'+id);
    var cnt = $('calendar-edit-'+id);

    new Ajax.Request('/calendar/' + id + '/delete/', {
                                                    onSuccess: function(r) {
                                                                            new Ajax.Updater('calendar-content', calendarUpdateURL);
                                                                           } 
                                                  })
}

function toggleView(type, id, onoff) {
    view = $(type + '-view-' + id);
    edit = $(type + '-edit-' + id);
    
    if (onoff) {
        set_visible(edit);
        set_invisible(view);
    } else {
        set_visible(view);
        set_invisible(edit);    
    }    
    /*  Add 'Now' and 'Today' buttons to each field via javascript
     *  Django normally does this onload but then it does not change dynamically added fields,
     *  so we're doing this every time user clicks on 'Edit'
     */
    DateTimeShortcuts.init();
}

function set_visible(obj) {
    obj.addClassName('visible');
    obj.removeClassName('invisible');
}

function set_invisible(obj){
    obj.addClassName('invisible');
    obj.removeClassName('visible');
}


function do_on_load()
{
    update_metasense();
    DateTimeShortcuts.init();
}

function enter_pressed(e){
    var keycode;
    if (window.event) keycode = window.event.keyCode; 
    else if (e) keycode = e.which; 
    else return false; 
    return (keycode == 13); 
}

addEvent(window, 'load', do_on_load);


function submit_event(id) {
    var frm = $('calendar-form-'+id);
    var cnt = $('calendar-edit-'+id);

    new Ajax.Request(frm.readAttribute('action'), {
                                                    parameters: frm.serialize(true),
                                                    onSuccess: function(r) {
                                                                            new Ajax.Updater('calendar-content', calendarUpdateURL);
                                                                           },
                                                    onFailure: function(r) {
                                                                            cnt.innerHTML = r.responseText;
                                                                            DateTimeShortcuts.init.defer(1);
                                                                           }
                                                  })
}


function update_metasense() {
    /*new Ajax.Request('http://metalab.at/metasense/status.html', {asynchronous:true, onFailure:function(){}, onException:function(){}, onSuccess:function(transport){ */
    new Ajax.Request('/metasense/status.html', {asynchronous:true, onFailure:function(){}, onException:function(){}, onSuccess:function(transport){ 
        oopen = $('presence_open');
        oclosed = $('presence_closed');
        odefunct = $('presence_defunct');
        if(transport.responseText.match("ffnet")) {
            set_visible(oopen);
            set_invisible(oclosed);
            set_invisible(odefunct);
          } else if( transport.responseText.match("niemand")){
            set_visible(oclosed);
            set_invisible(oopen);            
            set_invisible(odefunct);
        } else {
            set_invisible(oopen);
            set_invisible(oclosed);
            set_visible(odefunct);
        }
    }});
}
