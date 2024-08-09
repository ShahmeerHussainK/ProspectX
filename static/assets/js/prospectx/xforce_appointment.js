function xfroceAppointment(conf) {
    this.options = conf;

    // Chain constructor with call
    Prospectx.call(this, this.options);

}
xfroceAppointment.prototype.init = function () {
     this.init_appointment_calendar();
}

xfroceAppointment.prototype.init_appointment_calendar = function () {
    _calendar = $('#appointment_calendar').fullCalendar({
        // header: {
        //     left: 'prev,next today',
        //     center: 'title',
        //     right: 'agendaDay,agendaWeek,month'
        // },
        //
        // allDay: true,
        // editable: false,
        // selectable: true,
        // nextDay: '00:00',
        // eventDrop: function (event) {
        //     alert(event.title + " was dropped on " + event.start.toISOString());
        //
        //     if (!confirm("Are you sure about this change?")) {
        //         event.revert();
        //     }
        // },
        // select: function (start, end, allDay) {
        //
        //     var temp = new Date(end);
        //     temp.setDate(temp.getDate() - 1)
        //     $.ajax({
        //         type: 'GET',
        //         url: '/task/get_createtask_formsets',
        //         success: function (data) { // on success..
        //             $("#create_partial_formsets").html(data['html_form']);
        //             $('#link-formset').formset({
        //                 addText: 'Add Reminder',
        //                 deleteText: 'Remove Reminder'
        //             });
        //         },
        //         error: function (xhr, ajaxOptions, thrownError) { // on error..
        //             alert("error")
        //         },
        //         statusCode: {
        //             404: function () {
        //                 alert("page not found");
        //             }
        //         }
        //     });
        //     var now = new Date();
        //
        //
        //     var end_time = new Date();
        //     end_time.setHours(end_time.getHours() + 1);
        //
        //
        //     var options = {hour: "numeric", minute: "numeric"};
        //     var currentStartTime = now.toLocaleTimeString('en-US', options);
        //     var currentEndTime = end_time.toLocaleTimeString('en-US', options);
        //
        //     var start = moment(start, 'MM.DD.YYYY').format('MM/DD/YYYY');
        //     var end = moment(temp, 'MM.DD.YYYY').format('MM/DD/YYYY');
        //     start = start + ' ' + currentStartTime;
        //     // end = end + ' ' + currentEndTime;
        //     end = end + ' ' + currentStartTime;
        //     $('#startdatetime').val(start);
        //     $('#enddatetime').val(end);
        //
        //     $('#tasksModal').modal('show');
        //
        //
        //     _calendar.fullCalendar('unselect');
        // },
        // events: '/task/load_calendar/?event=' + self.events,
        // eventClick: function (event) {
        //     prospectxCalendar.prototype.update_cal_task(event)
        //
        // }

    })

}
