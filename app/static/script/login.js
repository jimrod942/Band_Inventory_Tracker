$(document).ready(function () {
    $('#signout').click(function () {
        $.ajax({
            type: 'POST',
            url:'/signout',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
            }),
            success: function (res) {
                console.log(res.response)
                window.location.href = "/";
            },
            error: function () {
                console.log('Error');
            }
        });
        alert("Successfully signed out :)");
    });

    $('#submit-login').click(function () {
        $.ajax({
            type: 'POST',
            url:'/login_search',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'username': $('#login-card').find('#username').val(),
                'password': $('#login-card').find('#password').val(),
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
});