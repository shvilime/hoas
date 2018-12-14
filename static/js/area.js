var $ = jQuery.noConflict();

// ================================= Common Events for html elements  =====================================
(function ($) {
    $(".btn-rosreestrnet").confirm({
        title: 'Подтверждение',
        content: 'Запросить бесплатные данные с сайта rosreestr.net?',
        buttons: {
            cancel: {
                text: 'Отменить',
                action: function () {
                }
            },
            confirm: {
                text: 'Запросить',
                btnClass: 'btn-green',
                action: function () {
                    let url = document.createElement('a');
                    url.href = this.$target.attr('href');
                    let params = $.urlParamsDecode(url.search);
                    params['csrfmiddlewaretoken'] = $.getCookie('csrftoken');
                    $.ajax({
                        url: url.pathname,
                        type: "POST",
                        dataType: 'json',
                        data: params,
                        success: function (json) {
                            $('#main-egrn').html(json['main']['egrn']);
                            let dt = new Date(json['main']['date_update'] * 1000);
                            $('#main-date').html(dt.toLocaleDateString());
                            $('#main-address').html(json['common']['address']);
                            let owners = json['owners']['length'];
                            if (owners > 0) {
                                $('#main-num-owners').html(owners);
                                for (var i = 0; i < owners; i++) {
                                    number = json['owners'][i]['number'];
                                    typerecord = json['owners'][i]['type'];
                                    let dt = new Date(json['owners'][i]['date'] * 1000);
                                    let txt = `<tr><td>${i + 1}</td><td>${typerecord}</td><td>${number}</td><td>${dt.toLocaleDateString()}</td></tr>`;
                                    $('#table-owners > tbody:last-child').after(txt);
                                }
                                $("#rosreestr-owners").removeClass('hidden');
                            } else {
                                $('#main-num-owners').html('Нет данных');
                            }
                            $('#area-type').html(json['common']['type']['title']);
                            $('#area-floor').html(json['common']['floor']);
                            $('#area-square').html(json['common']['area']['value']);

                            $("#rosreestr-common").removeClass('hidden');
                            $("#divider").removeClass('hidden');
                        },
                        error: function (xhr, errmsg, err) {
                            console.log(errmsg);
                        }
                    });
                }
            },
        }
    });

    $(".btn-apirosreestr").confirm({
        title: 'Подтверждение',
        content: 'Запросить ПЛАТНЫЕ данные с сайта apirosreestr.ru?',
        buttons: {
            cancel: {
                text: 'Отменить',
                action: function () {
                }
            },
            confirm: {
                text: 'Запросить',
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

    $(".btn-initialization").confirm({
        title: 'Подтверждение',
        content: 'Начать загрузку данных с росреестра?',
        buttons: {
            cancel: {
                text: 'Отменить',
                action: function () {
                }
            },
            confirm: {
                text: 'Запросить',
                btnClass: 'btn-green',
                action: function () {
                    let url = document.createElement('a');
                    url.href = this.$target.attr('href');
                    let params = $.urlParamsDecode(url.search);
                    params['csrfmiddlewaretoken'] = $.getCookie('csrftoken');
                    params['X-CSRFToken'] = $.getCookie('csrftoken');
                    $.getJSON(url.pathname, params, function (err, data) {
                        if (err != null) {
                            console.error(err);
                        } else {
                            let json = data;
                        }
                    });

                }
            },
        }
    });

})(jQuery);