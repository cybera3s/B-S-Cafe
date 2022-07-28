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

    function changeStatus(event, url="http://127.0.0.1:5000/admin/cashier_panel/order") {
        /*
            Send PUT request to change status of a order
        */
        $(this).parents('.dropdown').find('button').text($(this).text());

        let Data = {
            orderId: +$(this).data('order'),
            statusId: +$(this).attr('id'),
        };

        $.ajax({
            url: url,
            type: "PUT",
            contentType: "application/json",
            data: JSON.stringify(Data),
            success: function (response) {
                swal("Successful", "Order Status Changed!", "success", {
                    buttons: false,
                    timer: 2000,
                });
            },
            error: function (err) {
                console.log(err);
                 swal("Failed", "Something Went Wrong on changing status!", "error");
            }
        });
    };

    // click event for dropdown to change order status
    $(".content").on("click", ".dropdown-menu a", changeStatus);

    // click event for each row of table
    $('.data').on('click', getReceiptDetail)
});