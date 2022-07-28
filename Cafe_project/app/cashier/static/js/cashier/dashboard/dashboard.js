$(document).ready(function () {
    $('#user_info').on('mouseenter', () => {
        $('#user_info').css('box-shadow', '2px 2px 5px black')

    }).on('mouseleave', () => {
        $('#user_info').css('box-shadow', '2px 2px 12px gray')
    });

    $('form input').on('focus', () => {
        $('#save').removeClass('d-none')
    });

    function getChartInfo(url = 'http://127.0.0.1:5000/admin/cashier_panel/dashboard') {
        let xValues, yValues;
        url += `?getChartInfo=true`;
        $.get(url)
            .then(data => {
                new Chart("myChart", {
                    type: "line",
                    data: {
                        labels: data.labels,
                        datasets: [{
                            data: data.sum_receipts,
                            borderColor: "blue",
                            fill: true,
                            label: 'Income Of Last Seventh Days'
                        }]
                    },
                    min: 0,
                    options: {
                        legend: {display: true},
                        responsive: true,
                    }

                });
            })
    };

    getChartInfo();

})