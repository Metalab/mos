Ajax.Base.prototype.initialize = Ajax.Base.prototype.initialize.wrap(
function (callOriginal, options) {
    var headers = options.requestHeaders || {};
    headers["X-CSRFToken"] = getCookie("csrftoken");
    options.requestHeaders = headers;
    return callOriginal(options);
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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

function submit_form(type, id) {
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
            var notification = document.createElement('div');
            notification.className = 'notification success';
            notification.innerHTML = '<h3>Event '+ document.getElementById('calendarcontainer' + id).getElementsByClassName('name')[0].innerHTML +' deleted!</h3> ' + r.responseText;
            document.getElementById('calendarcontainer' + id ).parentNode.parentNode.insertBefore(notification, document.getElementById('calendarcontainer' + id ).parentNode);
            document.getElementById('calendarcontainer' + id ).parentNode.remove();
            new Ajax.Request('calendar-content', calendarUpdateURL, {
                method: 'get'
            })
        }
    })
}

function delete_entry(type, id) {
    container = $(type + 'container' + id);
    url = '/' + type + '/' + id + '/delete/';
    new Ajax.Request(url, {
        onSuccess: function(response) {
            container.remove();
        }
    })
}

function toggleView(type, id, onoff) {
    view = $(type + '-view-' + id);
    edit = $(type + '-edit-' + id);

    if (onoff) {
      set_visible(edit);
      if (view) {
          set_invisible(view);
        }
    } else {
      if (view) {
        set_visible(view);
      }
      set_invisible(edit);
    }
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

        var notification = document.createElement('div');
        notification.className = 'notification success';
        notification.innerHTML = '<h3>Event created or updated!</h3> ' + r.responseText;
        document.getElementById('calendar-update').parentNode.appendChild(notification);

        new Ajax.Updater('calendar-update', calendarUpdateURL, {
          method: 'get'
        });

//        new Notification('success', 'Event created/updated!', r.responseText).show();


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
