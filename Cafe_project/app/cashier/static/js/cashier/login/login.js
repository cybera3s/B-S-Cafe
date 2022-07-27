var alertList = document.querySelectorAll('.alert');
alertList.forEach(function (alert) {
    new bootstrap.Alert(alert)
});

$(document).ready(function () {

    $('.btn').on("mouseenter", () => {
        $('.btn').addClass("bg-primary")
    }).on("mouseleave", () => {
        $('.btn').removeClass("bg-primary")
    });
});
