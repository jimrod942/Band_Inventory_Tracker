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

    $('#submit-new-user').click(function () {
        $.ajax({
            type: 'POST',
            url:'/register_insert',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'username': $('#register-card').find('#username').val(),
                'password': $('#register-card').find('#password').val(),
                'admin': $('#register-card').find('#admin').val()
            }),
            success: function (res) {
                console.log(res.response)
                window.location.href="/Login";
            },
            error: function () {
                console.log('Error');
            }
        });
    });
});