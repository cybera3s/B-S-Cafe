$(document).ready(function () {

    $(".dropdown-menu").on('click', 'a', function () {
        $(this).parents('.dropdown').find('button').text($(this).text());
    });


    function getReceiptDetail(event, url = "http://127.0.0.1:5000/admin/cashier_panel/order") {
        event.preventDefault();
        let DataSend = {
            view: 'receipt_req',
            receipt_id: +this.id
        };

        $.ajax({
            url: url,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(DataSend),
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