$(document).ready(function () {
    var $signUpSubmitButton = $(".sign-up-button-js");
    var $signUpForm = $("#signupForm");
    var domain = "http://127.0.0.1:8000/";

    var $profileRegisterForm = $("#profileRegisterForm");
    var $saveProfileButton = $(".profile-submit-button-js");

    var successEnpoint = "accounts/success";
    var blankPageEnpoint = "accounts/signup/blank_page/";
    var successEnpoint = "accounts/success";
    var createUserEndpoint = "api/createUser/";
    var profileEndpoint = "accounts/profile";
    var saveProfileEndpoint = "api/save_profile/"

    $.fn.serializeObject = function () {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
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

    $saveProfileButton.click(function (e) {
        e.preventDefault();
        console.log(JSON.stringify($profileRegisterForm.serializeObject()))
        $.ajax({
            global: false,
            url: domain + saveProfileEndpoint,
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
            data: JSON.stringify($profileRegisterForm.serializeObject()),
            crossDomain: true
        }).done(
            function (data) {
                console.log("Success");
                window.location.replace(domain + successEnpoint);
            }
        ).fail(
            function (xhrResponse) {
                console.log("Failed");
            }
        );
    });


    $signUpSubmitButton.click(function (e) {
        e.preventDefault();
        $.ajax({
            url: domain + blankPageEnpoint,
            type: 'GET',
            crossDomain: true,
        }).done(function (data) {
            $.ajax({
                global: false,
                url: domain + createUserEndpoint,
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
                data: JSON.stringify($signUpForm.serializeObject()),
                crossDomain: true
            }).success(
                function (data) {
                    window.location.replace(domain + profileEndpoint);
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