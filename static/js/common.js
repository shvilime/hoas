var $ = jQuery.noConflict();

// ================================= jquery extend function =====================================
$.redirectPost = function (location, args) {
    var form = $('<form></form>');
    form.attr("method", "post");
    form.attr("action", location);
    $.each(args, function (key, value) {
        var field = $('<input></input>');
        field.attr("type", "hidden");
        field.attr("name", key);
        field.attr("value", value);
        form.append(field);
    });
    $(form).appendTo('body').submit();
};

$.getJSON = function (url, args, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.responseType = 'json';
    xhr.onload = function () {
        let status = xhr.status;
        if (status === 200) {
            callback(null, xhr.response);
        } else {
            callback(status);
        }
    };
    // let formData = new FormData();
    $.each(args, function (key, value) {
        // formData.append(key, value);
        xhr.setRequestHeader(key, value);
    });
    xhr.send();
};


$.urlParamsDecode = function (url) {
    let params = {};
    let match,
        pl = /\+/g,  // Regex for replacing addition symbol with a space
        search = /([^&=]+)=?([^&]*)/g,
        decode = function (s) {
            return decodeURIComponent(s.replace(pl, " "));
        },
        query = url.substring(1);
    while (match = search.exec(query)) {
        params[match[1]] = match[2];
    }
    return params;
};


$.getCookie = function (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

// ================================= Common Events for html elements  =====================================
(function ($) {
    /* SCRIPT TO SHOW CONFIRMATION WINDOW & SEND POST REQUEST FOR DELETE OWNER */
    $(".btn-delete-with-post").confirm({
        title: 'Подтверждение',
        content: 'Вы действительно хотите удалить данные?',
        buttons: {
            cancel: {
                text: 'Отменить',
                action: function () {
                }
            },
            confirm: {
                text: 'Удалить',
                btnClass: 'btn-red',
                action: function () {
                    let url = document.createElement('a');
                    url.href = this.$target.attr('href');
                    let params = $.urlParamsDecode(url.search);
                    params['csrfmiddlewaretoken'] = $.getCookie('csrftoken');
                    $.redirectPost(url.pathname, params);
                }
            },
        }
    });

})(jQuery);