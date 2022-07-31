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


    // remove category btn click event
    $('tr .delete-btn').click(deleteCategory);
});