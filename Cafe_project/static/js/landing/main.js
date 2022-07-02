/*jshint esversion: 6 */
$( document ).ready(function() {

    console.log("Document is ready!");
    const BASE_URL = 'http://127.0.0.1:5000';

    // Table click event
    $(".table-item").click(function () {
        $("#page-loader").empty();
        let tableId = $(this).attr('id');
        let target_url = 'http://127.0.0.1:5000/order/' + tableId;
        console.log(`table ${tableId} clicked`);

        $.get(
            target_url,
            function (data) {
                $("#page-loader").append(data);
                console.log(data.headers);
            }
        ).catch(err => console.log(err.responseText));
    });

    //  nav bar link on click event
    $(".nav-link-spa").click( function(e) {
        e.preventDefault();
        console.log("nav link clicked");
        let title = $(this).data("title");
        let endPoint = $(this).data("endpoint");
        $("#page-loader").empty();

        let target_url = 'http://127.0.0.1:5000/' + endPoint;
        $.ajax({
            url: target_url,
            type: "GET",
            success: function (response) {
                $("#page-loader").append(response);
                $(document).attr("title", title);
            }
    });

});

    // click event for add to cart btn
    $("#page-loader").on( "click", "button.add-to-cart-btn", function(event) {
        event.preventDefault();
        let item_id = $(this).data('itemid');

        console.log("add to cart clicked id: " + item_id);

        let table_id = $.cookie("table_id");
        let receipt_id = $.cookie("receipt_id");
        let target_url = BASE_URL + '/order/' + table_id;
        let order_count = $(`#count-${item_id}`).val();

        let data = {} // to store order detail data
        data['item_id'] = item_id;
        data['count'] = order_count;
        let postData = {    // to create a json object with required data
            order: data,
            table: table_id,
            receipt: receipt_id
        };

         $.post(
            target_url,
            {...postData},
            function (data) {

                console.log(data);
            }
        );

    });

    // show cart modal click event
    $("#cart-float-btn").click(function () {
        let target_url = BASE_URL + '/cart';

        $.get(
            target_url,
            function (data) {
                $('#cart-loader').empty();
                $('#cart-loader').append(data);
            }
        );
    });

    // function payment() {
    //     $('#page-loader').empty();
    //     let table_id = $.cookie("table_id");
    //     let receipt = $.cookie("receipt_id");
    //     let target_url = '{{ url_for('cart') }}';
    //     let postData = {
    //         receipt: receipt,
    //         table: table_id
    //     }
    //     $.ajax({
    //         url: target_url,
    //         type: 'POST',
    //         contentType: "application/json",
    //         data: JSON.stringify(postData),
    //         success: function (response) {
    //             $('#page-loader').append(response)
    //             swal('payment successful ', `Receipt Number : ${$.cookie('receipt_id')}`, 'success')
    //             $.removeCookie("receipt_id", {path: '/'});
    //         }
    //     })
    // }
});


