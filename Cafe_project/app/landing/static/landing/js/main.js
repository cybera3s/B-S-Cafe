/*jshint esversion: 6 */
$(document).ready(function () {

    console.log("Document is ready!");
    const BASE_URL = 'http://127.0.0.1:5000';

    function spaLoadData(e) {
        /*
            send a GET request to load content on page without refreshing
        */
        e.preventDefault();

        let title = $(this).data("title");
        let endPoint = $(this).data("endpoint");

        let target_url = 'http://127.0.0.1:5000/' + endPoint;
        $.ajax({
            url: target_url,
            type: "GET",
            success: function (response) {
                $("#page-loader").empty();
                $("#page-loader").append(response);
                $(document).attr("title", title);   // set title of page
            },
            error: function (err) {
                let errMsg = 'Something went wrong on loading content, try again later'
                swal("Failed", errMsg, "error");
            }
        });

    };

    function tableSelect() {
        /*
            Send a get request with provided table id
            if request is successful then append the returned data from server to #page_loader element
        */
        let tableId = +$(this).attr('id');
        let target_url = BASE_URL + '/order/' + tableId;

        $.ajax({
            url: target_url,
            method: 'get',
            success: function (data, status, xhr) {
                if (xhr.status === 200) {
                    $("#page-loader").empty();
                    $("#page-loader").append(data);

                }
                ;

            },
            error: function (err, status) {
                console.log(err, status);
                if (err.status === 400) {
                    let errorMsg = `${err.responseText}`;
                    swal("Failed", errorMsg, "error");
                    return;
                }
                let errorMsg = `Something went wrong\n${err.status} \n${err.statusText}`;
                swal("Failed", errorMsg, "error");
            }
        })
    };

    function addToCart(event) {
        /*
            get orders data from page then send post request to add order to cart
        */
        event.preventDefault();
        // get order data
        let itemId = $(this).data('itemid');
        let itemCount = $(this).siblings(".itemCount").val();
        let itemName = $(this).siblings(".itemName").text();
        let itemPrice = $(this).siblings(".itemPrice");
        let priceData = itemPrice.children().length > 0 ? itemPrice.data() : itemPrice.text()  // {...} or $5
        // extract final price and original price
        let finalPrice = 0, price;
        if (typeof priceData === 'object') {
            finalPrice = priceData.finalprice;
            price = priceData.price;
        } else {
            price = priceData.replace("$", '');
        }

        const url = BASE_URL + "/order/" + itemId
        // define data for post request
        let data = {
            itemId: +itemId,
            itemName: itemName,
            itemCount: +itemCount,
            itemPrice: +price,
            finalPrice: +finalPrice
        }
        $.ajax({
            url: url,
            type: "post",
            dataType: "json",
            contentType: 'application/json',
            data: JSON.stringify(data),

            success: function (data) {
                swal("Successful", "Added To Cart!", "success", {
                    buttons: false,
                    timer: 1500,
                });
            },
            error: function (err) {
                swal("Failed", err.responseText, "error")
                    .then(res => {
                        window.location.reload();
                    })
            }
        });

    };

    function showCart(e) {
        /*
            send GET request to load orders on cart
        */
        e.preventDefault();
        let target_url = BASE_URL + '/cart';

        $.get(target_url)
            .done(function (data) {
                $('#cart-loader').empty();
                $('#cart-loader').append(data);
            })
            .fail(function (err) {
                console.log(err.responseText)
                swal("Failed", err.responseText, "error")
            });
    };

    function payment() {
        /*
            send post request to cart view to finalize the payment
        */
        let totalPrice = $("#totalPrice").text();
        let finalPrice = $("#finalPrice").text();

        let target_url = BASE_URL + '/cart';


        $.ajax({
            url: target_url,
            type: 'POST',
            data: {
                totalPrice: +totalPrice,
                finalPrice: +finalPrice,
            },
            success: function (response) {
                let receiptId = $.cookie('receipt_id');     // get receipt id from cookie
                $('#page-loader').empty();
                $('#page-loader').append(response);
                swal(
                    'Successful',
                    `Payment Was Successful!\nReceipt Number : ${receiptId}`,
                    'success'
                );
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

    // get empty tables
    function getAvailableTables() {
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

    //  nav bar link on click event
    $(".nav-link-spa").click(spaLoadData);

    // Table select click event
    $(".table-item").click(tableSelect);

    //    Add to cart button click event
    $("#page-loader").on("click", "button.add-to-cart-btn", addToCart);

    //     show cart modal click event
    $("#page-loader").on("click", "#cart-float-btn", showCart);

    // payment button click event
    $("#pay-btn").click(payment);


    // Contact us Page
    function sendContactUsForm(e) {
        e.preventDefault();

        let url = "/contact_us"; // send the form data here.
        let csrfToken = $(this).children('#csrf_token').val();  // get contact us form csrf token

        $.ajax({
            // Inject our CSRF token into our AJAX request.
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrfToken)
                }
            },
            type: "POST",
            url: url,
            data: $(this).serialize(), // serializes the form's elements.
            success: function (data) {
                swal("Successful", data, "success");
                $("form")[0].reset();   // clear form inputs
            },
            error: function (err) {
                console.log(err);
                swal("Failed", err, "error");
            }
        });
    };

    $("#page-loader").on("submit", "#contactUsForm", sendContactUsForm);


});


