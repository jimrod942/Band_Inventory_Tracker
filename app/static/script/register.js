$(document).ready(function () {

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
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
});