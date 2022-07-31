$(document).ready(function () {
    const BASE_URL = 'admin/cashier_panel/tables';

    // show change state button on mouse hover to busy tables
    $('.tables').on('mouseenter', function () {

        $state = $(this).find(".state")

        if ($state.html() === 'Busy') {
            $(this).find(".change_state").fadeIn(600);
            $(this).find(".show-info").fadeIn(600);
        }
    }).on('mouseleave', function () {
        $(this).css("opacity", '1.0').find(".change_state").fadeOut(100);
        $(this).css("opacity", '1.0').find(".show-info").fadeOut(100);
    });

    // animate opacity of table image on mouse hover on Change State Button
    $('.change_state,.show-info').on('mouseenter', function () {

        $(this).parent().find('img').css("opacity", '0.5')

    }).on('mouseleave', function () {
        $(this).parent().find('img').css("opacity", '1.0')
    });

    function getTableOrders(event, url = url_root) {
        let id = $(this).attr('id');
        url += BASE_URL;

        $.ajax({
            url: url,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({get_info: true, id: +id}),
            success: function (response) {
                // show beautiful alert by Sweetalert lib
                $(".modal-body").empty()
                $(".modal-body").append(response)
            }
        })

    }

    function changeStatus(event, url = url_root) {
        let id = $(this).attr('id');
        url += BASE_URL;

        $.ajax({
            url: url,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({get_info: false, id: +id}),
            success: function (response) {
                // show beautiful alert by Sweetalert lib
                swal({
                    position: 'top',
                    icon: 'success',
                    title: `The Table #${id} is Free Now!`,
                    showConfirmButton: true,

                })
                $(`span#${id}`).text('Free')
            }
        })

    }

    // Send AJAX request on click on change state btn
    $(".change_state").on('click', changeStatus);

    // Send AJAX request on click on show info btn
    $(".show-info").on('click', getTableOrders);
});
