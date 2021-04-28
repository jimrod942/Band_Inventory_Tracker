$(document).ready(function () {
    $('#signout').click(function () {
        $.ajax({
            type: 'POST',
            url:'/signout',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
            }),
            success: function (res) {
                console.log(res.response);
                // location.reload();
                window.location.href = "/";
                alert("Successfully signed out :)");
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#submit-insert-instrument').click(function () {
        $.ajax({
            type: 'POST',
            url:'/instrument_insert',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'instrumentid': $('#insert-div').find('#ins-instrID-field').val(),
                'instrument_type': $('#insert-div').find('#ins-type-field').val(),
                'brand': $('#insert-div').find('#ins-brand-field').val()
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

    $('#submit-update-instrument').click(function () {
        const instID = $('#update-div').find('#upd-instrID-field').val();
        console.log("UPDATE INSTRUMENT, ID = " + instID);
        $.ajax({
            type: 'POST',
            url:'/instrument_update/' + instID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'instrumentid': $('#update-div').find('#upd-instrID-field').val(),
                'instrument_type': $('#update-div').find('#upd-type-field').val(),
                'brand': $('#update-div').find('#upd-brand-field').val()
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

    // does deletes
    $('.remove').click(function () {
        const remove = $(this)
        console.log('REMOVE INSTRUMENT, ID = ' + remove.data('source'))
        $.ajax({
            type: 'POST',
            url: '/instrument_delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#submit-search-instrument').click(function () {
        const instID = $('#search-div').find('#search-instrID-field').val();
        $.ajax({
            type: 'POST',
            url:'/instrument_search/' + instID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'instrumentid': $('#search-div').find('#search-instrID-field').val()
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