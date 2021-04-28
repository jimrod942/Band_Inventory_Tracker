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

    $('#submit-insert-maintenance').click(function () {
        $.ajax({
            type: 'POST',
            url:'/maintenance_insert',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'instrumentid': $('#insert-div').find('#ins-instrID-field').val(),
                'send_date': $('#insert-div').find('#ins-send-field').val(),
                'return_date': $('#insert-div').find('#ins-return-field').val(),                
                'maintenance_location': $('#insert-div').find('#ins-location-field').val(),
                'cost': $('#insert-div').find('#ins-cost-field').val(),
                'maintenance_id': $('#insert-div').find('#ins-mainID-field').val()
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

    $('#submit-update-maintenance').click(function () {
        const mainID = $('#update-div').find('#upd-mainID-field').val();
        console.log("UPDATE Maintenance, ID = " + mainID);
        $.ajax({
            type: 'POST',
            url:'/maintenance_update/' + mainID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'instrumentid': $('#update-div').find('#upd-instrID-field').val(),
                'send_date': $('#update-div').find('#upd-send-field').val(),
                'return_date': $('#update-div').find('#upd-return-field').val(),                
                'maintenance_location': $('#update-div').find('#upd-location-field').val(),
                'cost': $('#update-div').find('#upd-cost-field').val(),
                'maintenance_id': $('#update-div').find('#upd-mainID-field').val()
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

    $('#submit-search-maintenance').click(function() {
        const mainID = $('#search-div').find('#sea-mainID-field').val();
        console.log("SEARCH Maintenance, ID = " + mainID);
        $.ajax({
            type: 'POST',
            url: '/maintenance_search/' + mainID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'maintenance_id': $('#search-div').find('#sea-mainID-field').val()
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


    $('.remove').click(function () {
        const remove = $(this)
        console.log('REMOVE Maintenance, ID = ' + remove.data('source'))
        $.ajax({
            type: 'POST',
            url: '/maintenance_delete/' + remove.data('source'),
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