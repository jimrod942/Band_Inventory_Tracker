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
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
        alert("Successfully signed out :)");
    });
});