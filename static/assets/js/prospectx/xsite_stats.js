function Xsite_Statistics(conf) {

    this.options = conf;

    // Chain constructor with call

    Prospectx.call(this, this.options);
}

Xsite_Statistics.prototype.init = function () {
    let self = this;

    $(document).ready(function () {
        Stats_7_Days();
    });

};

function refresh_graph() {
    $('#loading').show();
    $('#graph').hide();
    $("#chart").empty();
}

function make_start_Date(daysPrior) {
    var date = new Date(startDate);
    date.setDate(date.getDate() - daysPrior);
    return date.toISOString().substring(0, 10);
}

function Stats_7_Days() {
    refresh_graph();
    FetchStatistics(make_start_Date(6));
}

function Stats_30_Days() {
    refresh_graph();
    FetchStatistics(make_start_Date(29));
}

function Stats_90_Days() {
    refresh_graph();
    FetchStatistics(make_start_Date(89));
}

function Stats_180_Days() {
    refresh_graph();
    FetchStatistics(make_start_Date(179));
}

function Stats_365_Days() {
    refresh_graph();
    FetchStatistics(make_start_Date(364));
}

function Stats_all_time_Days() {
    refresh_graph();
    console.log(site_creation_date);
    FetchStatistics(site_creation_date);
}


function formatDate(date) {
    var monthNames = [
        "01", "02", "03",
        "04", "05", "06", "07",
        "08", "09", "10",
        "11", "12"
    ];

    var day = date.getDate();
    var monthIndex = date.getMonth();
    var year = date.getFullYear();

    return year + '-' + monthNames[monthIndex] + '-' + day;
}


function combine_dates(data, sizeOfArray) {

    stats = [];
    for (var i = 0; i < sizeOfArray; i++) {
        var visitors = parseInt(data[i]['visitors']);
        for (var j = 0; j < sizeOfArray; j++) {
            if (i !== j) {
                if (data[i]['date'] === data[j]['date']) {
                    visitors = visitors + parseInt(data[j]['visitors']);
                }
            }
        }
        stats.push({"date": data[i]['date'], "visitors": visitors})

    }
    var uniqueStats = [];
    $.each(stats, function (i, el) {
        var check = 0;
        for (j = 0; j < uniqueStats.length; j++) {
            if (el['date'] === uniqueStats[j]['date']) {
                check = check + 1
            }
        }
        if (check === 0) {
            uniqueStats.push(el);
        }
    });
    return uniqueStats;
}


function FetchStatistics(startdate) {

    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/xsite/local_time_statistics/" + data + "/" + startdate + "/",
        success: function (data) { // on success..
            var sizeOfArray = data['list_data'].length;
            for (var i = 0; i < sizeOfArray; i++) {
                var utcDate = data['list_data'][i]['date'];  // ISO-8601 formatted date returned from server
                var localDate = new Date(utcDate);
                data['list_data'][i]['date'] = formatDate(localDate);
            }
            uniqueStats = combine_dates(data['list_data'], sizeOfArray);
            $('#loading').hide();
            $('#graph').show();
            $('#total_visitors').html(data['total_visitors']);
            $('#avg_time').html(data['avg_time']);
            $('#percentage_mobile_visitors').html(data['percentage_mobile_visitors'] + "%");
            $('#total_leads').html(data['total_leads']);
            Morris.Area({
                element: 'chart',
                data: uniqueStats,
                xkey: 'date',
                ykeys: ['visitors'],
                labels: ['Visitors', 'Date'],
                xLabelFormat: function (d) {
                    var months = new Array(12);
                    months[0] = "JAN";
                    months[1] = "FEB";
                    months[2] = "MAR";
                    months[3] = "APR";
                    months[4] = "MAY";
                    months[5] = "JUN";
                    months[6] = "JUL";
                    months[7] = "AUG";
                    months[8] = "SEP";
                    months[9] = "OCT";
                    months[10] = "NOV";
                    months[11] = "DEC";

                    return months[d.getMonth()] + " " + d.getDate();
                },
                xLabels: 'day',
                fillOpacity: 0.4,
                hideHover: 'auto',
                behaveLikeLine: true,
                resize: true,
                pointFillColors: ['#ffffff'],
                pointStrokeColors: ['#7367F0'],
                lineColors: ['#7367F0']
            });
            // config = {
            // data: uniqueStats,
            // xkey: 'date',
            // ykeys: ['visitors'],
            // labels: ['Visitors', 'Date'],
            // xLabelFormat: function (d) {
            //     var months = new Array(12);
            //     months[0] = "JAN";
            //     months[1] = "FEB";
            //     months[2] = "MAR";
            //     months[3] = "APR";
            //     months[4] = "MAY";
            //     months[5] = "JUN";
            //     months[6] = "JUL";
            //     months[7] = "AUG";
            //     months[8] = "SEP";
            //     months[9] = "OCT";
            //     months[10] = "NOV";
            //     months[11] = "DEC";
            //
            //     return months[d.getMonth()] + " " + d.getDate();
            // },
            // xLabels: 'day',
            // fillOpacity: 0.4,
            // hideHover: 'auto',
            // behaveLikeLine: true,
            // resize: true,
            // pointFillColors: ['#ffffff'],
            // pointStrokeColors: ['black'],
            // lineColors: ['#337ab7']
            // };
            //
            // config.element = 'morris-line';
            // Morris.Line(config);
        },
        error: function (xhr, ajaxOptions, thrownError) { // on error..
            var err = JSON.parse(xhr.responseText);
            toastr.error(err.message);
        },
        statusCode: {
            404: function () {
                alert("page not found");
            }
        }
    });
}