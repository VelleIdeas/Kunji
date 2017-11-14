$(document).ready(function () {
    var $logOutButton = $(".logout_button_js");
    var domain = "http://127.0.0.1:8000/";
    var login_endpoint = "accounts/login"

    $logOutButton.click(function (e) {
        e.preventDefault()
        $.ajax({
            url: domain + 'api/logOut/',
            type: 'GET',
            crossDomain: true,
        }).done(function (data) {
            console.log("User logged out successfully")
            window.location.replace(domain + login_endpoint);
        }).fail(
            function (xhrResponse) {
                console.log("failed");
            }
        );
    });
});