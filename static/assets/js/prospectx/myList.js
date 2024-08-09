function prospectxList(conf) {
    this.options = conf;
    // this.calendar;

    // Chain constructor with calla
    Prospectx.call(this, this.options);
    // var calendarcus = null;

}


prospectxList.prototype.init = function () {
    let self = this;
    $("#datatable-list-view").on("click", ".task-title", this.update_list_task);
    $(document).on("click", ".sidebar_options", function () {
        let action = $(this).attr('id') || 'all';
        self.list_view_clicked(action);
    });
    // Task update button on list
    $(document).on("click", ".task-edit", this.update_task_btn);
    $(document).on("click", ".task-delete", this.delete_task_btn);
    $(document).on("click", "#btnmodaldeletetask", this.delete_it);

    // Task delete button on list

}


prospectxList.prototype.list_view_clicked = function (action) {

    let url = '/task/get_list_data/' + action + '/';

    if ($(this).text().trim() == "List View") {

    }
    $.ajax({
        type: 'GET',
        url: url,
        success: function (data) {

            prospectxList.prototype.create_sidebar(data)
            prospectxList.prototype.create_task_table(data["tasks"], data["subusers"])
            prospectxList.prototype.init_datatable()


        },
        error: function (xhr, ajaxOptions, thrownError) { // on error..
            alert("error")
        },
        statusCode: {
            404: function () {
                alert("page not found");
            }
        }
    });
    $("#calendar_view").removeClass('d-block');
    $("#calendar_view").addClass('d-none');
    $("#list_view").removeClass('d-none');
    $("#list_view").addClass('d-block');

}

prospectxList.prototype.create_sidebar = function (data) {
    var completed_task = JSON.parse(data["completed_tasks"])
    var daily_due_tasks = JSON.parse(data["daily_due_tasks"])
    var future_pending_tasks = JSON.parse(data["future_pending_tasks"])
    var past_due_tasks = JSON.parse(data["past_due_tasks"])
    var future_count = data["future_count"]

    console.log("future_pending_tasks");
    console.log(future_pending_tasks);
    var table_body = $(".custom_task_table");
    table_body.empty();
    get_role = localStorage.getItem('role')

    //daily task

    var heading_html = '<tr class="task_custom_title daily-due-task">\n' +
        '<th id="daily_task" class="custom_sidbar_heading sidebar_options"><a style="color: #4090CB;" href="#">Daily Task </a><span class="float-right">' + daily_due_tasks.length + '</span>\n' +
        '</th>\n' +
        '</tr>';
    table_body.append(heading_html);
    // if (get_role == 'Admin User') {
    daily_due_tasks.forEach(function (task, index) {
        console.log(task["title"]);
        let assign_to = "";
        if (task["assign_to__user__first_name"] === null) {
            task["assign_to__user__first_name"]
            assign_to = "Not assigned"
        } else {
            task["assign_to__user__first_name"]
            assign_to = task["assign_to__user__first_name"]
        }
        var row_html = '<tr><td>' + assign_to + '<span class="float-right">' + task["task_count"] + '</span></td></tr>';
        table_body.append(row_html)
    });
    // }


    // Past Due Task

    var heading_html = '<tr class="task_custom_title daily-due-task">\n' +
        '<th class="custom_sidbar_heading sidebar_options" id ="past_due_task"><a style="color: #4090CB;" href="#">Past Due Task</a> <span class="float-right">' + past_due_tasks.length + '</span>\n' +
        '</th>\n' +
        '</tr>';
    table_body.append(heading_html);
    // if (get_role == 'Admin User') {
    past_due_tasks.forEach(function (task, index) {
        console.log(task["title"])
        let assign_to = "";
        if (task["assign_to__user__first_name"] === null) {
            task["assign_to__user__first_name"]
            assign_to = "Not assigned"
        } else {
            task["assign_to__user__first_name"]
            assign_to = task["assign_to__user__first_name"]
        }
        var row_html = '<tr><td>' + assign_to + '<span class="float-right">' + task["task_count"] + '</span></td></tr>';
        table_body.append(row_html)
    });
    // }

    // Future pending task

    var heading_html = '<tr class="task_custom_title daily-due-task">\n' +
        '<th class="custom_sidbar_heading sidebar_options" id="future_pending_task"><a style="color: #4090CB;" href="#">Future Pending Task</a><span class="float-right">' + future_count + '</span>\n' +
        '</th>\n' +
        '</tr>';
    table_body.append(heading_html);
    // if (get_role == 'Admin User') {

    future_pending_tasks.forEach(function (task, index) {
        console.log(task["title"]);
        let assign_to = "";
        if (task["assign_to__user__first_name"] === null) {
            task["assign_to__user__first_name"]
            assign_to = "Not assigned"
        } else {
            task["assign_to__user__first_name"]
            assign_to = task["assign_to__user__first_name"]
        }
        var row_html = '<tr><td>' + assign_to + '<span class="float-right">' + task["task_count"] + '</span></td></tr>';
        table_body.append(row_html)
    });
    // }
    // }

    // Completed Task

    var heading_html = '<tr class="task_custom_title daily-due-task">\n' +
        '<th class="custom_sidbar_heading sidebar_options" id="completed_task"><a style="color: #4090CB;" href="#">Completed Task</a><span class="float-right">' + completed_task.length + '</span>\n' +
        '</th>\n' +
        '</tr>';
    table_body.append(heading_html);
    // if (get_role == 'Admin User') {
    completed_task.forEach(function (task, index) {
        console.log(task["title"]);
        let assign_to = "";
        if (task["assign_to__user__first_name"] === null) {
            task["assign_to__user__first_name"]
            assign_to = "Not assigned"
        } else {
            task["assign_to__user__first_name"]
            assign_to = task["assign_to__user__first_name"]
        }
        var row_html = '<tr><td>' + assign_to + '<span class="float-right">' + task["task_count"] + '</span></td></tr>';
        table_body.append(row_html)
    });
    // }

};

prospectxList.prototype.create_task_table = function (tasks, subusers) {

    var actual_table = $(".main-task-table");
    actual_table.empty();
    if ($.fn.DataTable.isDataTable("#datatable-list-view")) {
        $('#datatable-list-view').dataTable().fnClearTable();
        $('#datatable-list-view').dataTable().fnDestroy();
    }

    var table_header = '<thead>\n' +
        '                            <tr>\n' +
        '                                <th>#</th>\n' +
        '                                <th>Name</th>\n' +
        '                                <th>Temperature</th>\n' +
        '                                <th>Is Completed ?</th>\n' +
        '                                <th>Start Date</th>\n' +
        '                                <th>End Date</th>\n' +
        '                                <th>Action</th>\n' +
        '                            </tr>\n' +
        '                            </thead><tbody>';

    actual_table.html(table_header)

    tasks.forEach(function (task, index) {
        console.log("complete task obj");
        console.log(task)
        table_data = '<tr class="prow"><td  class="task-id">' + (index + 1) + '</td><td title-id = "' + task["id"] + '"  id=\"task' + task["id"] + '\" class="task-title"><a href="#">' + task["title"] + '</a></td><td>';
        // var title_html = $('<td class="task-title"><a href="#">' + task["title"] + '</a></td><td>').attr("id", "id" + task["id"]);
        // table_data = table_data + title_html;
        if (task["temperature"] == "cold") {
            table_data += '<span class="text-primary font-12"><i\n' +
                'class="mdi mdi-checkbox-blank-circle mr-1"></i> Cold</span>'
        } else if (task["temperature"] == "warm") {
            table_data += '<span class="text-warning font-12"><i\n' +
                'class="mdi mdi-checkbox-blank-circle mr-1"></i> Warm</span>'
        } else if (task["temperature"] == "hot") {
            table_data += '<span class="text-danger font-12"><i\n' +
                'class="mdi mdi-checkbox-blank-circle mr-1"></i> Hot</span>'
        }
        table_data += '</td>';
        table_data += '<td>';
        if (task["is_completed"] == true) {
            table_data += '<span class="badge badge-success font-12">Completed</span>'
        } else if (task["is_completed"] == false) {
            table_data += '<span class="badge badge-primary font-12">Pending</span>'
        }
        table_data += '</td>'
        var start_format_date = moment(task["start_date_time"]).format('MM/DD/YYYY h:mm A');
        var end_format_date = moment(task["end_date_time"]).format('MM/DD/YYYY h:mm A');
        table_data += '<td>' + start_format_date +
            '</td>';
        table_data += '<td>' + end_format_date +
            '</td>';

        table_data += '<td>\n' +
            '              <div class=" " role="group" aria-label="Basic example">\n' +
            '                   <button task-id="task' + task["id"] + '" type="button" class="btn btn-sm btn-primary task-edit" data-toggle="tooltip"\n' +
            '                       data-placement="top" title="" data-original-title="Edit"><i\n' +
            '                       class="mdi mdi-grease-pencil"></i></button>\n' +
            '                   <button task-id="' + task["id"] + '" type="button" class="btn btn-sm btn-danger task-delete" data-toggle="modal"  href="#btndeleteModal"><i\n' +
            '                       class="mdi mdi-trash-can-outline "></i></button>\n' +
            '               </div>\n' +
            '           </td></tr>';

        actual_table.append(table_data)
        console.log("_____")
        var get_id_element = $("#task" + task["id"])
        get_id_element.data({
            "id": task["id"],
            "title": task["title"],
            "assign_to": task["assign_to"],
            "description": task["description"],
            "all_day": task["is_all_day_task"],
            "is_completed": task["is_completed"],
            "start":start_format_date,
            "end": end_format_date,
            "temperature": task["temperature"],
            "subusers": subusers
        })
    });
    // prospectxList.prototype.init_datatable()

    actual_table.append('</tbody>')


};
prospectxList.prototype.update_list_task = function () {
    console.log("clicked item is")
    console.log($(this).data());
    var event = $(this).data();
    // var event_id = $(this).siblings('.task-id').text();
    // alert(parseInt(event_id))

    prospectxCalendar.prototype.update_cal_task(event)
    // prospectxList.prototype.create_task_table();
};

prospectxList.prototype.delete_task_btn = function () {

    var obj = $(this).attr('task-id');
    $('#btnmodaldeletetask').attr('task-id' , obj);

    $('#btndeleteModal').modal('show');

};


prospectxList.prototype.delete_it = function () {

    var obj = $(this).attr('task-id');

     $.ajax({
        type: 'GET',
        url: "/task/delete_task/" + obj + "/",
        success: function (data) { // on success..
            // $('#updatedeleteModal').modal('hide');
            $('#btndeleteModal').modal('hide');
            toastr.success("Task Deleted Successfully");
            if($("#calendar_view").is(":visible")){
                 _calendar.fullCalendar('refetchEvents');
             }
             else {
                 prospectxList.prototype.list_view_clicked("all");
             }
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
prospectxList.prototype.update_task_btn = function () {

    var task_id = $(this).attr('task-id');
    let event_data = $('#' + task_id).data();

    prospectxCalendar.prototype.update_cal_task(event_data)


};

// load daily tasks

prospectxList.prototype.init_datatable = function () {

    $("#datatable-list-view").DataTable();
};
