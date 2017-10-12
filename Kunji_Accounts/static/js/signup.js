$(document).ready(function () {
    var $submitButton = $(".sign-up-button-js");
    var $form = $("#signupForm");
    var domain = "http://127.0.0.1:8000/";

    $.fn.serializeObject = function() {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function() {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };

    $submitButton.click(function (e) {
        e.preventDefault()
        $.ajax({
            url: domain + 'accounts/signup/blank_page/',
            type: 'GET',
            crossDomain: true,
        }).done(function (data) {
            $.ajax({
                global: false,
                url: domain + "api/createUser/",
                headers: {
                    "X-CSRFToken": $.cookie('csrftoken'),
                },
                xhrFields: {
                    withCredentials: true
                },
                cache: false,
                type: 'POST',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify($form.serializeObject()),
                crossDomain: true
            }).done(
                function (data) {

                }
            ).fail(
                function (xhrResponse) {
                    // If fail, just call the failure callback, no cookie to set
                }
            );
        }).fail(
            function (xhrResponse) {
                console.log("failed");
            }
        );
    });
});