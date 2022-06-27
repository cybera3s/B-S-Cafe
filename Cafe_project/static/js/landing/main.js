/*jshint esversion: 6 */
$( document ).ready(function() {
    console.log( "Document is ready!" );

    function table_select(table_id) {
    let target_url = 'http://127.0.0.1:5000/order';
    $("#page-loader").empty();
    $.ajax({
        url: `${target_url}/${table_id}`,
        type: "GET",
        success: function (response) {
            $("#page-loader").append(`${response}`)
        }
    })
}

//  nav bar link on click event
    $(".navigation-link > a").click( function(e) {
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

// add FoodItem to Order (ajax)
function order(item_id) {
    let table_id = $.cookie("table_id") // get table id from cookies to include in json file
    let receipt_id = $.cookie("receipt_id") // get receipt id from cookies to include in json file
    let target_url = `http://127.0.0.1:5000/order/${table_id}`
    let order_count = $(`#count-${item_id}`).val()
    let data = {} // to store order detail data
    data['item_id'] = item_id;
    data['count'] = order_count;
    let postData = {    // to create a json object with required data
        order: data,
        table: table_id,
        receipt: receipt_id
    };
    $.ajax({        // ajax request to send order details to flask
        url: target_url,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(postData),
        success: function (resp) {
            swal('سفارش موفق', 'محصول با موفقیت به سبد خرید اضافه شد!', 'success')
        }
    })
}

function cart_loader() {
    let target_url = "{{ url_for('cart') }}"
    $.ajax({        // ajax request to send order details to flask
        url: target_url,
        type: "GET",
        success: function (resp) {
            $('#cart-loader').empty();
            $('#cart-loader').append(resp);
        }
    })
}

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

