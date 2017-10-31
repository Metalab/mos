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
        set_invisible(view);
    } else {
        set_visible(view);
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
    // Do nothing. *Thumbleweed crossed the web*
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
                                                                            new Ajax.Updater('calendar-content', calendarUpdateURL, {
                                                                              method: 'get'})
                                                                           },
                                                    onFailure: function(r) {
                                                                            cnt.innerHTML = r.responseText;
                                                                            DateTimeShortcuts.init.defer(1);
                                                                           }
                                                  })
}
