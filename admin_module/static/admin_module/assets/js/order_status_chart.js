$(document).ready(function () {
    var data = orderStatusChartData.map(function (item) {
        return {
            label: item.label,
            data: item.data,
            color: item.color
        };
    });

    $.plot("#dashboard-pie-chart-sources", data, {
        series: {
            pie: {
                show: true,
                radius: 1,
                label: {
                    show: true,
                    radius: 3 / 4,
                    formatter: function (label, series) {
                        return "<div style='font-size:11px; text-align:center; padding:2px; color:#fff;'>" +
                            Math.round(series.percent) + "%</div>";
                    },
                    background: {
                        opacity: 0.6
                    }
                }
            }
        },
        legend: {
            show: false
        }
    });
});