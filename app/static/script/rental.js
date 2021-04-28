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

    $('#submit-insert-rental').click(function () {
        $.ajax({
            type: 'POST',
            url:'/rental_insert',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'rental_id' : $('#insert-div').find('#ins-rentID-field').val(),
                'instrument_id' : $('#insert-div').find('#ins-instrID-field').val(),
                'net_id' : $('#insert-div').find('#ins-netID-field').val(),
                'date_out' : $('#insert-div').find('#ins-dateOUT-field').val(),
                'date_in' : $('#insert-div').find('#ins-dateIN-field').val()
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

    $('#submit-search-rental').click(function () {
        $.ajax({
            type: 'POST',
            url: '/rental_search',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'rental_id' : $('#search-div').find('#search-rentID-field').val()
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

    $('#submit-update-rental').click(function () {
        // const instID = $('#upd-instrID-field').val();
        const rentID = $('#update-div').find('#upd-rentID-field').val();
        console.log("UPDATE Rentals, ID = " + rentID);
        $.ajax({
            type: 'POST',
            url:'/rental_update/' + rentID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'rental_id' : $('#update-div').find('#upd-rentID-field').val(),
                'instrument_id' : $('#update-div').find('#upd-instrID-field').val(),
                'net_id' : $('#update-div').find('#upd-netID-field').val(),
                'date_out' : $('#update-div').find('#upd-dateOUT-field').val(),
                'date_in' : $('#update-div').find('#upd-dateIN-field').val()
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
        console.log('REMOVE Rental, ID = ' + remove.data('source'))
        $.ajax({
            type: 'POST',
            url: '/rental_delete/' + remove.data('source'),
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