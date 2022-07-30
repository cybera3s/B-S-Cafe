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
})
