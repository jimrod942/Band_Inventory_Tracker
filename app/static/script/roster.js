$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal

    $('#submit-insert-student').click(function () {
        $.ajax({
            type: 'POST',
            url:'/student_insert',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'net_id': $('#insert-div').find('#ins-netID-field').val(),
                'first_name': $('#insert-div').find('#ins-fname-field').val(),
                'last_name': $('#insert-div').find('#ins-lname-field').val(),
                'grade': $('#insert-div').find('#ins-grade-field').val(),
                'section':$('#insert-div').find('#ins-section-field').val()
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

    $('#submit-update-student').click(function () {
        const netID = $('#update-div').find('#upd-netID-field').val();
        console.log("UPDATE STUDENT, ID = " + netID);
        $.ajax({
            type: 'POST',
            url:'/student_update/' + netID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'net_id': $('#update-div').find('#upd-netID-field').val(),
                'first_name': $('#update-div').find('#upd-fname-field').val(),
                'last_name': $('#update-div').find('#upd-lname-field').val(),
                'grade': $('#update-div').find('#upd-grade-field').val(),
                'section': $('#update-div').find('#upd-section-field').val()
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

    $('#submit-search-student').click(function () {
        const netID = $('#search-div').find('#search-netID-field').val();
        console.log("SEARCH STUDENT, ID = " + netID);
        $.ajax({
            type: 'POST',
            url:'/student_search',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'net_id': $('#search-div').find('#search-netID-field').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error')
            }
        });
    });

    // does deletes
    $('.remove').click(function () {
        const remove = $(this)
        console.log('REMOVE STUDENT, ID = ' + remove.data('source'))
        $.ajax({
            type: 'POST',
            url: '/student_delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#test-btn').click(function () {
        $.ajax({
            type: 'POST',
            url: '/roster_to_instruments',
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