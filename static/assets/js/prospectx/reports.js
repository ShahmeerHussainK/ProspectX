function Reports(conf) {

    this.options = conf;
    // Chain constructor with call
    Prospectx.call(this, this.options);

}

Reports.prototype.init = function () {
    let self = this;
    Reports.prototype.init_Datatable();
    let data_param = {type: 'GET', url: 'report_history_data', 'page': 0, 'page2': 0};
    Reports.prototype.get_report_data(data_param);
    setInterval(function () {
        info = $('#import_history_datatable').DataTable().page.info();
        info2 = $('#export_history_datatable').DataTable().page.info();
        let data_param = {type: 'GET', url: 'report_history_data', 'page': info.page, 'page2': info2.page};
        Reports.prototype.get_report_data(data_param);
    }, 5000);

    $(document).on('click', '.export_btn', function () {
        var id = $(this).attr("mydata");
        let data_param = {type: 'GET', url: 'export_to_excel/' + id + '/'};
        Reports.prototype.export_btn_clicked(data_param);
        toastr.info("We are working on your import history export. Once completed you can download the file from the Export History option in the Reports Section.")
    });

};

Reports.prototype.init_Datatable = function () {
    $('#import_history_datatable, #export_history_datatable').DataTable({
        lengthChange: false,
        bFilter: false,
        "order": [[ 0, "desc" ]]
    });
};

Reports.prototype.get_report_data = function (data_param) {

    $.ajax({
        type: data_param.type,
        url: data_param.url,
        success: function (data) { // on success..
            var import_history = data['import_history_data'];
            var export_history = data['export_history_data'];
            // var status = data['status'];

            actual_table = $(".import_table");

            actual_table.empty();
            $('#import_history_datatable').dataTable().fnClearTable();
            $('#import_history_datatable').dataTable().fnDestroy();
            var table_header = '<thead>\n' +
                '                            <tr>\n' +
                '                                <th>Date</th>\n' +
                '                                <th>Campaign</th>\n' +
                '                                <th>Imported</th>\n' +
                '                                <th>Tagged/Updated</th>\n' +
                '                                <th>Skip Traced</th>\n'+
                '                                <th>Skipped</th>\n' +
                '                                <th>Status</th>\n' +
                '                                <th>Import Option</th>\n' +
                '                                <th>Fail Reason</th>\n' +
                '                                <th>Action</th>\n' +
                '                            </tr>\n' +
                '                            </thead><tbody>';

            actual_table.html(table_header);

            import_history.forEach(function (item, index) {
                if (item['overall_status'] === false) {
                    markup = "<tr>\n" +
                        "                                                                                        <td>" + item['list__created_at'] + "</td>\n" +
                        "                                                                                        <td>" + item['list__list_name'] + "</td>\n" +
                        "                                                                                        <td>" + item['imported'] + "</td>\n" +
                        "                                                                                        <td>" + item['updated'] + "</td>\n" +
                        "                                                                                        <td>" + item['skip_traced'] + "</td>\n" +
                        "                                                                                        <td><a href=\"skipped_history/" + item['pk'] + "/\">" + item['skipped'] + "</a></td>\n" +
                        "                                                                                        <td><span class=\" badge badge-warning \">"+item['processing_type']+"</span></td>\n" +
                        "                                                                                        <td>" + item['list__import_option'] + "</td>\n" +
                        "                                                                                        <td>" + item['fail_reason'] + "</td>\n" +
                        "                                                                                        <td>\n" +
                        "                                                                                        </td>\n" +
                        "                                                                                    </tr></tbody>";
                } else {
                    markup = "<tr>\n" +
                        "                                                                                        <td>" + item['list__created_at'] + "</td>\n" +
                        "                                                                                        <td>" + item['list__list_name'] + "</td>\n" +
                        "                                                                                        <td>" + item['imported'] + "</td>\n" +
                        "                                                                                        <td>" + item['updated'] + "</td>\n" +
                        "                                                                                        <td>" + item['skip_traced'] + "</td>\n" +
                        "                                                                                        <td><a href=\"skipped_history/" + item['pk'] + "/\">" + item['skipped'] + "</a></td>\n" +
                        "                                                                                        <td><span class=\"badge badge-success \">Completed</span></td>\n" +
                        "                                                                                        <td>" + item['list__import_option'] + "</td>\n" +
                        "                                                                                        <td>" + item['fail_reason'] + "</td>\n" +
                        "                                                                                        <td>\n" +
                        "                                                                                            <button type=\"button\" mydata=\"" + item['pk'] + "\" class=\"btn btn-default border-secondary btn-sm mr-1 export_btn btn_downlod_color\" \n" +
                        "                                                                                                    data-toggle=\"tooltip\" data-placement=\"top\" title=\"\"\n " +
                        "                                                                                                    data-original-title=\"Export\"><i\n" +
                        "                                                                                                    class=\"fa fa-download fa-1x \"></i></button>" +
                        "                                                                                        </td>\n" +
                        "                                                                                    </tr></tbody>";
                }
                actual_table.append(markup);
            });

            actual_table2 = $(".export_table");
            actual_table2.empty();
            $('#export_history_datatable').dataTable().fnClearTable();
            $('#export_history_datatable').dataTable().fnDestroy();
            var table_header2 = '<thead>\n' +
                '                            <tr>\n' +
                '                                <th>Date</th>\n' +
                '                                <th>File Name</th>\n' +
                '                                <th>Status</th>\n' +
                '                                <th>Action</th>\n' +
                '                            </tr>\n' +
                '                            </thead><tbody>';

            actual_table2.html(table_header2);

            export_history.forEach(function (item, index) {
                markup = "<tr>\n" +
                    "                                                                                        <td>" + item['created_at'] + "</td>\n" +
                    "                                                                                        <td>" + item['file_name'] + "</td>\n" +
                    "                                                                                        <td>Completed</td>\n" +
                    "                                                                                        <td><button onclick=\"window.location.href = \'/media/exported_files/" + item['file_name'] + "\'\" type=\"button\" class=\"btn btn-primary\"> \n" +
                    "                                                                                         Download </button>" +
                    "                                                                                        </td>\n" +
                    "                                                                                    </tr></tbody>";

                actual_table2.append(markup);

            });

            Reports.prototype.init_Datatable();
            var oTable = $('#import_history_datatable').dataTable();
            oTable.fnPageChange(data_param.page);
            var oTable2 = $('#export_history_datatable').dataTable();
            oTable2.fnPageChange(data_param.page2);
        },
        error: function (xhr, ajaxOptions, thrownError) { // on error..
            // alert("in fail");
            let err = JSON.parse(xhr.responseText);
            console.log(err);
        },
        statusCode: {
            404: function () {
                alert("page not found");
            }
        }
    });
};


Reports.prototype.export_btn_clicked = function (data_param) {

    $.ajax({
        type: data_param.type,
        url: data_param.url,
        success: function (data) { // on success..
            let data_param = {type: 'GET', url: 'report_history_data'};
            Reports.prototype.get_report_data(data_param);

        },
        error: function (xhr, ajaxOptions, thrownError) { // on error..
            // alert("in fail");
            let err = JSON.parse(xhr.responseText);
            console.log(err);
        },
        statusCode: {
            404: function () {
                alert("page not found");
            }
        }
    });
};