/*jshint esversion: 6 */
$( document ).ready(function() {

    console.log("Document is ready!");
    const BASE_URL = 'http://127.0.0.1:5000';

    function tableSelect() {
        /*
            Send a get request with provided table id
            if request is successful then append the returned data from server to #page_loader element
        */
        let tableId = $(this).attr('id');
        let target_url =  BASE_URL + '/order/' + tableId;

        $.ajax({
            url: target_url,
            method: 'get',
            success: function (data, status, xhr){
                if (xhr.status === 200){
                    $("#page-loader").empty();
                    $("#page-loader").append(data);

                    let receipt_id = xhr.getResponseHeader('receipt_id');
                    $.cookie('receipt_id', receipt_id);
                    $.cookie('table_id', tableId)

                };

            },
            error: function (err, status) {
                console.log(err, status);
                if (err.status === 400){
                    let errorMsg = `${err.responseText}`;
                    swal("Failed", errorMsg, "error");
                    return;
                }
                let errorMsg = `Something went wrong\n${err.status} \n${err.statusText}`;
                 swal("Failed", errorMsg, "error");
            }
        })
    }

    // Table select click event
    $(".table-item").click(tableSelect);

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

                swal("Successful", "Added To Cart!", "success", {
                    buttons: false,
                    timer: 1500,
                });

            },
            error: function(err){
                console.log(err);
                swal("Failed", err.responseText, "error")
                    .then(res => {
                        window.location.reload();
                    })

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


    function paymentBtnClickEvent() {
        /*
            send post request to cart view to finalize the payment
        */


        // console.log('pay btn clicked');

        let table_id = $.cookie("table_id");
        let receipt = $.cookie("receipt_id");
        let target_url = BASE_URL + '/cart';

        let postData = {
            receipt: receipt,
            table: table_id
        }

        $.ajax({
            url: target_url,
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify(postData),
            success: function (response) {
                $('#page-loader').empty();
                $('#page-loader').append(response);
                swal(
                    'payment successful ',
                    `Receipt Number : ${$.cookie('receipt_id')}`,
                    'success'
                );
                $.removeCookie("receipt_id", {path: '/'});

            },
            error: function (error) {
                console.log(error);
                swal(
                    'Payment Failed ',
                    `Something went wrong`,
                    'error'
                );
            }
        })
    };

    // payment button click event
    $("#pay-btn").click(paymentBtnClickEvent);

    // get empty tables
    function getAvailableTables(){
        let URL = BASE_URL + '/tables';

        $.ajax({
            method: 'GET',
            url: URL,
            accept: 'application/json',
            success: function (response) {
                console.log(response);
            },
            error: function (err) {
                console.log(err);
            }
        })
    }
});


