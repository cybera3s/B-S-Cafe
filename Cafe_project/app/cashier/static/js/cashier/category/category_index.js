$(document).ready(function () {
    const BASE_URL = 'admin/cashier_panel/categories';

    function deleteCategory(e, url = url_root) {
        /*
            Send DELETE request to remove a category
        */
        e.preventDefault();

        let row = $(this).parents('tr')
        let catId = row.attr('id');
        url += BASE_URL + `?category_id=${catId}`;

        $.ajax({
            url: url,
            method: 'DELETE',
            success: function (data) {
                swal('Done', data, 'success');
                $(row).remove();
            },
            error: function (error) {
                console.log(error);
                swal('Failed', data, 'error');
            }
        });

    };

    function getCategoryModalForm(e, url = url_root) {
        /*
            Send GET request to fill out edit category modal
        */
        e.preventDefault();
        let row = $(this).parents('tr');
        let catId = row.attr('id');

        url += BASE_URL + `/${catId}`;

        $.ajax({
            url: url,
            method: 'GET',
            success: function (data) {
                $(".modal-body").empty();
                $(".modal-body").append(data);
            },
            error: function (error) {
                console.log(error);
                swal('Failed', 'Something went Wrong!' + error, 'error');
            }
        });
    }

    function submitModifyCategory(event, url = url_root){
        /*
            Send PUT request to update a category
        */
        event.preventDefault();

        let catId = $(this).children('#id').val()
        url += BASE_URL + `/${catId}` ;
        let csrfToken = $(this).children('#csrf_token').val();  // get form csrf token

        $.ajax({
            // Inject our CSRF token into our AJAX request.
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrfToken);
                }
            },
            type: "PUT",
            url: url,
            data: $(this).serialize(), // serializes the form's elements.
            success: function (data) {
                swal("Successful", data, "success")
                    .then(result => {
                        window.location.reload();   // reload page on click ok alert
                    });
            },
            error: function (err) {
                console.log(err);
                let errors = err.responseJSON;
                swal("Failed", "Please Correct Errors!", "error");
                // bind errors with their fields
                for (let field in errors) {
                    let f = $("form").find(`#${field}`);
                    f.addClass('is-invalid').next().text(errors[field].join(' '))
                }

            }
        });

    }

    // remove category btn click event
    $('tr .delete-btn').click(deleteCategory);
});