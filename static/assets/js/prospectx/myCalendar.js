function prospectxCalendar(conf) {
    this.options = conf;
    // this.calendar;
    this.events = 'all';

    // Chain constructor with call
    Prospectx.call(this, this.options);
    // var calendarcus = null;

}


prospectxCalendar.prototype.init = function () {
    let self = this
    this.init_calendar();
    // prospectxCalendar.prototype.cal_init();
    // Update List Task
    $("#calendar-btn").click(function () {
        _calendar.fullCalendar('refetchEvents');
        $("#calendar_view").removeClass('d-none');
        $("#calendar_view").addClass('d-block');
        $("#list_view").removeClass('d-block');
        $("#list_view").addClass('d-none');

    });

    // calendar filters
    $(".cal-filter").click(function () {

        self.events = $(this).attr("action")

        self.init_calendar();
        // _calendar.fullCalendar('refetchEvents');
        _calendar.fullCalendar('destroy');
        self.init_calendar();
    })


};



prospectxCalendar.prototype.init_calendar = function () {
    let self = this;
    _calendar = $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'agendaDay,agendaWeek,month'
        },

        allDay: true,
        editable: false,
        selectable: true,
        nextDay: '00:00',
        eventDrop: function (event) {
            alert(event.title + " was dropped on " + event.start.toISOString());

            if (!confirm("Are you sure about this change?")) {
                event.revert();
            }
        },
        select: function (start, end, allDay) {
            // alert(start)
            // alert(end)
            var temp = new Date(end);
            temp.setDate(temp.getDate() - 1)
            $.ajax({
                type: 'GET',
                url: '/task/get_createtask_formsets',
                success: function (data) { // on success..
                    $("#create_partial_formsets").html(data['html_form']);
                    $('#link-formset').formset({
                        addText: 'Add Reminder',
                        deleteText: 'Remove Reminder'
                    });
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
            var now = new Date();


            var end_time = new Date();
            end_time.setHours(end_time.getHours() + 1);


            var options = {hour: "numeric", minute: "numeric"};
            var currentStartTime = now.toLocaleTimeString('en-US', options);
            var currentEndTime = end_time.toLocaleTimeString('en-US', options);

            var start = moment(start, 'MM.DD.YYYY').format('MM/DD/YYYY');

            var end = moment(temp, 'MM.DD.YYYY').format('MM/DD/YYYY');
            start = start + ' ' + currentStartTime;
            // end = end + ' ' + currentEndTime;
            end = end + ' ' + currentStartTime;
            $('#startdatetime').val(start);
            $('#enddatetime').val(end);

            $('#tasksModal').modal('show');


            _calendar.fullCalendar('unselect');
        },
        // displayEventTime: false,
        timezone: 'local',
        events: '/task/load_calendar/?event=' + self.events,


        eventClick: function (event) {
            prospectxCalendar.prototype.update_cal_task(event)

        }

    })

    // var event = _calendar.getEventById(1);

}


//change events
// call refetch

prospectxCalendar.prototype.update_cal_task = function (event) {
    console.log("event start")
    console.log(event)
    console.log("event end")
    var e = event["title"];

    $('#update_modal_id').val(event["id"]);
    $('#hidden_link').val(window.location.host + "/task/all_tasks_calendar/" + event["id"] + "/");
    $('#duplicate_task').attr("href", "/task/duplicate_task/" + event["id"] + "/");
    $('#id').val(event["id"]);
    $('#update_modal_title').val(event["title"]);
    var $select = $('#update_assign_to');
    $select.find('option')
        .remove()
        .end()
        .append('<option value="">Select</option>')
        .val('0')
    ;
    var sub_users_array = event["subusers"];
    console.log(event["subusers"])
    sub_users_array.forEach(function (user, index) {
        $option = $('<option value="' + user["id"] + '">' + user['email'] + '</option>');
        if(event["assign_to"]!=null){
            if (user["id"] === event["assign_to"]["id"]) {
            $option.prop('selected', true);
        } else if (user["id"] === event["assign_to"]) {
            $option.prop('selected', true);
        }
        }

        $select.append($option);
    })
    $('#assign_to').val(event["assign_to"]);
    $('#description').val(event["description"]);

    var start_format_date = moment(event["start"]).format('MM/DD/YYYY h:mm A');

    var end_format_date = moment(event["end"]).format('MM/DD/YYYY h:mm A');
    var temp = new Date(end_format_date);
    temp.setDate(temp.getDate() + 1)
    $('#startdatetime2').val(start_format_date)
    $('#enddatetime2').val(end_format_date)
    if (event["allDay"]) {
        $('#update_is_all_day_task').prop("checked", true)
    } else {
        $('#update_is_all_day_task').prop("checked", false)
    }
    if (event["is_completed"]) {
        $('#is_completed').prop("checked", true)
    } else {
        $('#is_completed').prop("checked", false)
    }

    if (event["temperature"] === "warm") {
        $("#update_radio2").prop("checked", true);
    } else if (event["temperature"] === "cold") {
        $('#update_radio1').prop("checked", true);
    } else if (event["temperature"] === "hot") {
        $('#update_radio3').prop("checked", true);
    }
    $.ajax({
        type: 'GET',
        url: '/task/get_task_formsets/' + event["id"] + '/',
        success: function (data) { // on success..
            $("#update_partial_formsets").html(data['html_form']);
            $('#updatetasksModal').modal('show');
            $('#llink-formset').formset({
                addText: 'Add Reminder',
                deleteText: 'Remove Reminder'
            });
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
    $(document).on('click', '.delete-row', function () {
        $(this).parent().remove();
    });


}


