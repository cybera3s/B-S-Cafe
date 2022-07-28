$(document).ready(function () {

    $(".dropdown-menu").on('click', 'a', function () {
        $(this).parents('.dropdown').find('button').text($(this).text());
    });


    function getReceiptDetail(event, url = "http://127.0.0.1:5000/admin/cashier_panel/order") {
        /*
            Send GET request to get receipt detail by ID
        */
        event.preventDefault();
        url += `?receipt_id=${+this.id}`;   // set query parameter

        $.ajax({
            url: url,
            type: "GET",
            success: function (response) {
                $("#receipt_modal").empty();
                $("#receipt_modal").append(response)
            },
            error: function (err) {
                console.log(err);
                Swal('Failed', 'Something Went wrong', 'error');
            }
        });
    }

    // click event for each row of table
    $('.data').on('click', getReceiptDetail)
});