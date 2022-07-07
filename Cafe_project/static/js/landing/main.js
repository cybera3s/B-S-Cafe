/*jshint esversion: 6 */
$( document ).ready(function() {

    console.log("Document is ready!");
    const BASE_URL = 'http://127.0.0.1:5000';

    // Table select click event
    $(".table-item").click(function () {
        $("#page-loader").empty();
        let tableId = $(this).attr('id');
        let target_url =  BASE_URL + '/order/' + tableId;
        console.log(`table ${tableId} clicked`);

        $.ajax({
            url: target_url,
            method: 'post',
            data: {
                'action': "select_table"
            },
            success: function (data, status, xhr){
                if (xhr.status === 200){
                    $("#page-loader").append(data);

                    let receipt_id = xhr.getResponseHeader('receipt_id');
                    $.cookie('receipt_id', receipt_id);
                    $.cookie('table_id', tableId)

                };

            },
            error: function (err, status) {
                console.log(err, status);
                let errorMsg = '<h1>Something went wrong</h1>'
                $("#page-loader").append(errorMsg);
            }
        })
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

    ///////////       Add to cart button click event      ////////////////
    $("#page-loader").on( "click", "button.add-to-cart-btn", function(event) {
        event.preventDefault();

        let itemId = $(this).prev().data('itemid');
        let itemCount = $(this).prev().val();
        let receiptId = $.cookie('receipt_id');
        const url = BASE_URL + "/order/" + itemId
        // console.log(`${itemCount} of ${itemId}`);
        // define data for post request
        let data = {
            action: 'add_to_cart',
            itemId: itemId,
            itemCount: +itemCount,
            receiptId: +receiptId,
        }
          $.ajax({
            url: url,
            type: "post",
            dataType: "json",
            contentType: 'application/json',
            data: JSON.stringify(data),

            success: function (data){

                    if (data.status === 200){
                        swal("Successful", "Updated Cart!", "success", {
                            buttons: false,
                            timer: 1500,
                        });
                    } else if (data.status === 201) {
                        swal("Successful", "Added to Cart!", "success", {
                            buttons: false,
                            timer: 1500,
                        });
                    }

                    console.log(data.msg);
            },
            error: function(err){
                console.log(err);
            }
         });



    });

    ///////////////      show cart modal click event        ////////////
    $("#page-loader").on( "click", "#cart-float-btn", function(event){
        // console.log('Cart Item clicked');
        let receiptId = $.cookie('receipt_id');
         let target_url = BASE_URL + '/cart' + `?receipt_id=${receiptId}`;

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


