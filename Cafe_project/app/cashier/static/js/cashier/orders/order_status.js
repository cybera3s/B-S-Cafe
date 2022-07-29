$(document).ready(function () {

    function updateOrders(e, url = url_root) {
        e.preventDefault();
        let statusId = document.URL.slice(-1);
        url += 'admin/cashier_panel/order/status/' + statusId
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'updateTable': true,
            },
            success: function (response) {
                $("#row_table").html(response);
            }
        });

    };

    function search(event) {
        event.preventDefault();
        $rows = $('#Table > tbody tr');
        let val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();

        $rows.show().filter(function () {
            var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
            return !~text.indexOf(val);
        }).hide();
    }

    $("#update-btn").on('click', updateOrders);

    // $("#search-btn").on('keyup', search);
    $("#search-btn").keyup(search);

});