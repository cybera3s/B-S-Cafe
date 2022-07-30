$(document).ready(function () {
    const listMenuItemUrl = "admin/cashier_panel/list_menu"

    function getMenuItem(event, url = url_root) {
        /*
            Send GET request to get menu item by id and fill the modal
         */
        event.preventDefault();

        let menuItemId = $(this).attr('id');
        url += listMenuItemUrl + `?menuItemId=${menuItemId}`;
        $.ajax({
            url: url,
            type: "GET",
            success: function (response) {
                $("#item_modal").empty();
                $('#item_modal').append(response)
            }
        });
    };

    function removeMenuItem(event, url = url_root) {
        /*
            Send DELETE request to Remove Menu item
        */
        event.preventDefault();
        let id = +$(this).attr('id');
        url += listMenuItemUrl + `?menuItemId=${id}`

        $.ajax({
            url: url,
            type: "DELETE",
            success: function (response) {
                swal(
                    'Successful',
                    'Item Deleted Successfully!',
                    'success'
                )
                $(`tr#${id}`).remove();

            },
            error: function (err) {
                console.log(err);
                swal(
                    'Failed',
                    'Could Not Delete Item!',
                    'error'
                )
            },
        });
    }

    // click event to get menu item and fill modal
    $('.edit').on('click', getMenuItem);

    // click event to remove menu item
    $('.delete-item').on('click', removeMenuItem);


    function showUploadedImage() {
        /*
            validate and show uploaded image
        */
        let file = $(this).prop('files')[0];

        // image type validation
        if (!/image\/*/.test(file.type)) {
            swal(
                'Failed',
                'Wrong type for image input!',
                'error'
            );
            $(this).focus();
            return;
        };

        let tempURL = URL.createObjectURL(file);

        $("#targetImage").attr('src', tempURL);
        $("label[for='targetImage']").text(file.name);

    };

    function sendEditMenuItemForm(e, url = url_root) {
        /*
            Send form fields data with POST request
        */
        e.preventDefault();

        url += listMenuItemUrl; // send form data here.
        let csrfToken = $(this).children('#csrf_token').val();  // get contact us form csrf token

        $.ajax({
            // Inject our CSRF token into our AJAX request.
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrfToken);
                }
            },
            type: "POST",
            url: url,
            data: new FormData(this), // serializes the form's elements.
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                swal("Successful", data, "success")
                    .then(result => {
                        window.location.reload();   // reload page on click ok alert
                    });
            },
            error: function (err) {
                let errors = err.responseJSON;

                swal("Failed", "Please Correct Errors!", "error");

                for (let field in errors) {
                    let f = $("#editMenuItemForm").find(`#${field}`);
                    f.addClass('is-invalid').next().text(errors[field].join(' '))
                }

            }
        });
    };

    // show uploaded image in img tag on change of file input
    $('.content').on('change', "#image", showUploadedImage);

    // submit event of edit menu item
    $(".content").on("submit", "#editMenuItemForm", sendEditMenuItemForm);

})
